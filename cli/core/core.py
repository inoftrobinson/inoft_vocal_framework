import json
from pathlib import Path
import logging
import boto3
import botocore
import click
import troposphere
from botocore.exceptions import ClientError

from inoft_vocal_framework.cli.core.core_clients import CoreClients


class Core(CoreClients):
    def __init__(self):
        super().__init__()
        self._iam_role = None
        self._credentials_arn = None
        self.role_name = "InoftVocalFrameworkLambdaExecution"

    def get_lambda_function(self, function_name: str):
        return self.lambda_client.get_function(FunctionName=function_name)

    def get_lambda_function_versions(self, function_name: str) -> list:
        try:
            response = self.lambda_client.list_versions_by_function(FunctionName=function_name)
            return response.get('Versions', list())
        except Exception as e:
            print(f"Error while getting the versions of the lambda function {function_name} : {e}")
            return list()

    def create_lambda_function(self, bucket=None, s3_key: str = None, function_name: str =None, handler=None,
                               description: str = "Inoft Vocal Framework Deployment",
                               timeout: int = 30, memory_size: int = 512, publish: bool = True, runtime=None, local_zip: bool = None):
        """
        Given a bucket and key (or a local path) of a valid Lambda-zip, a function name and a handler, register that Lambda function.
        """
        kwargs = dict(
            FunctionName=function_name,
            Runtime=runtime,
            Role=self.credentials_arn,
            Handler=handler,
            Description=description,
            Timeout=timeout,
            MemorySize=memory_size,
            Publish=publish,
            # VpcConfig=vpc_config,
            # DeadLetterConfig=dead_letter_config,
            # Environment={'Variables': aws_environment_variables},
            # KMSKeyArn=aws_kms_key_arn,
            # TracingConfig={
            #    'Mode': 'Active' if self.xray_tracing else 'PassThrough'
            # }
        )
        if local_zip:
            kwargs['Code'] = {
                'ZipFile': local_zip
            }
        else:
            kwargs['Code'] = {
                'S3Bucket': bucket,
                'S3Key': s3_key
            }

        response = self.lambda_client.create_function(**kwargs)

        resource_arn = response['FunctionArn']
        version = response['Version']

        """
        # If we're using an ALB, let's create an alias mapped to the newly
        # created function. This allows clean, no downtime association when
        # using application load balancers as an event source.
        # See: https://github.com/Miserlou/Zappa/pull/1730
        #      https://github.com/Miserlou/Zappa/issues/1823
        if use_alb:
            self.lambda_client.create_alias(
                FunctionName=resource_arn,
                FunctionVersion=version,
                Name=ALB_LAMBDA_ALIAS,
            )

        if self.tags:
            self.lambda_client.tag_resource(Resource=resource_arn, Tags=self.tags)
        """
        return resource_arn

    def create_stack_template(self, lambda_arn: str,
                                lambda_name,
                                api_key_required,
                                iam_authorization,
                                authorizer,
                                cors_options=None,
                                description=None,
                                endpoint_configuration=None
                            ):
        """
        Build the entire CF stack.
        Just used for the API Gateway, but could be expanded in the future.
        """

        auth_type = "NONE"
        if iam_authorization and authorizer:
            logger.warn("Both IAM Authorization and Authorizer are specified, this is not possible. "
                        "Setting Auth method to IAM Authorization")
            authorizer = None
            auth_type = "AWS_IAM"
        elif iam_authorization:
            auth_type = "AWS_IAM"
        elif authorizer:
            auth_type = authorizer.get("type", "CUSTOM")

        # build a fresh template
        self.cf_template = troposphere.Template()
        self.cf_template.add_description('Automatically generated with Zappa')
        self.cf_api_resources = []
        self.cf_parameters = {}

        restapi = self.create_api_gateway_routes(
                                            lambda_arn,
                                            api_name=lambda_name,
                                            api_key_required=api_key_required,
                                            authorization_type=auth_type,
                                            authorizer=authorizer,
                                            cors_options=cors_options,
                                            description=description,
                                            endpoint_configuration=endpoint_configuration
                                        )
        return self.cf_template

    def create_api_gateway_routes(self, lambda_arn: str, api_name: str = None, description: str = None, api_key_required=False,
                                  authorization_type="NONE", authorizer=None, cors_options=None, endpoint_configuration=None):

        import troposphere.apigatewayv2 as apigateway
        rest_api = troposphere.Template()
        api_resource = apigateway.Api(title=api_name or lambda_arn.split(":")[-1])
        api_resource.title = "inoftvocalframework-test"
        rest_api.description = description or "Created automatically by the Inoft Vocal Framework"
        rest_api.add_resource(api_resource)

        self.cf_template.add_resource(rest_api)

        root_id = troposphere.GetAtt(rest_api, 'RootResourceId')
        invocation_prefix = "aws" if boto3.Session.region_name != "us-gov-west-1" else "aws-us-gov"
        invocations_uri = ('arn:' + invocation_prefix + ':apigateway:' + boto3.Session.region_name +
                           ':lambda:path/2015-03-31/functions/' + lambda_arn + '/invocations')

        ##
        # The Resources
        ##
        authorizer_resource = None
        if authorizer:
            authorizer_lambda_arn = authorizer.get('arn', lambda_arn)
            lambda_uri = 'arn:{invocation_prefix}:apigateway:{region_name}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'.format(
                invocation_prefix=invocation_prefix,
                region_name=self.boto_session.region_name,
                lambda_arn=authorizer_lambda_arn
            )
            authorizer_resource = self.create_authorizer(
                restapi, lambda_uri, authorizer
            )

        self.create_and_setup_methods(restapi,
                                      root_id,
                                      api_key_required,
                                      invocations_uri,
                                      authorization_type,
                                      authorizer_resource,
                                      0
                                      )

        if cors_options:
            self.create_and_setup_cors(restapi,
                                       root_id,
                                       invocations_uri,
                                       0,
                                       cors_options
                                       )

        resource = troposphere.apigateway.Resource('ResourceAnyPathSlashed')
        self.cf_api_resources.append(resource.title)
        resource.RestApiId = troposphere.Ref(restapi)
        resource.ParentId = root_id
        resource.PathPart = "{proxy+}"
        self.cf_template.add_resource(resource)

        self.create_and_setup_methods(restapi,
                                      resource,
                                      api_key_required,
                                      invocations_uri,
                                      authorization_type,
                                      authorizer_resource,
                                      1
                                      )  # pragma: no cover

        if cors_options:
            self.create_and_setup_cors(restapi,
                                       resource,
                                       invocations_uri,
                                       1,
                                       cors_options
                                       )  # pragma: no cover
        return restapi

    def update_stack(self, name, working_bucket, wait=False, update_only=False, disable_progress=False):
        """
        Update or create the CF stack managed by Zappa.
        """
        capabilities = []

        template = name + '-template-' + str(int(time.time())) + '.json'
        with open(template, 'wb') as out:
            out.write(bytes(self.cf_template.to_json(indent=None, separators=(',',':')), "utf-8"))

        self.upload_to_s3(template, working_bucket, disable_progress=disable_progress)
        if self.boto_session.region_name == "us-gov-west-1":
            url = 'https://s3-us-gov-west-1.amazonaws.com/{0}/{1}'.format(working_bucket, template)
        else:
            url = 'https://s3.amazonaws.com/{0}/{1}'.format(working_bucket, template)

        tags = [{'Key': key, 'Value': self.tags[key]}
                for key in self.tags.keys()
                if key != 'ZappaProject']
        tags.append({'Key':'ZappaProject','Value':name})
        update = True

        try:
            self.cf_client.describe_stacks(StackName=name)
        except botocore.client.ClientError:
            update = False

        if update_only and not update:
            print('CloudFormation stack missing, re-deploy to enable updates')
            return

        if not update:
            self.cf_client.create_stack(StackName=name,
                                        Capabilities=capabilities,
                                        TemplateURL=url,
                                        Tags=tags)
            print('Waiting for stack {0} to create (this can take a bit)..'.format(name))
        else:
            try:
                self.cf_client.update_stack(StackName=name,
                                            Capabilities=capabilities,
                                            TemplateURL=url,
                                            Tags=tags)
                print('Waiting for stack {0} to update..'.format(name))
            except botocore.client.ClientError as e:
                if e.response['Error']['Message'] == 'No updates are to be performed.':
                    wait = False
                else:
                    raise

        if wait:
            total_resources = len(self.cf_template.resources)
            current_resources = 0
            sr = self.cf_client.get_paginator('list_stack_resources')
            progress = tqdm(total=total_resources, unit='res', disable=disable_progress)
            while True:
                time.sleep(3)
                result = self.cf_client.describe_stacks(StackName=name)
                if not result['Stacks']:
                    continue  # might need to wait a bit

                if result['Stacks'][0]['StackStatus'] in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']:
                    break

                # Something has gone wrong.
                # Is raising enough? Should we also remove the Lambda function?
                if result['Stacks'][0]['StackStatus'] in [
                                                            'DELETE_COMPLETE',
                                                            'DELETE_IN_PROGRESS',
                                                            'ROLLBACK_IN_PROGRESS',
                                                            'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
                                                            'UPDATE_ROLLBACK_COMPLETE'
                                                        ]:
                    raise EnvironmentError("Stack creation failed. "
                                           "Please check your CloudFormation console. "
                                           "You may also need to `undeploy`.")

                count = 0
                for result in sr.paginate(StackName=name):
                    done = (1 for x in result['StackResourceSummaries']
                            if 'COMPLETE' in x['ResourceStatus'])
                    count += sum(done)
                if count:
                    # We can end up in a situation where we have more resources being created
                    # than anticipated.
                    if (count - current_resources) > 0:
                        progress.update(count - current_resources)
                current_resources = count
            progress.close()

        try:
            os.remove(template)
        except OSError:
            pass

        self.remove_from_s3(template, working_bucket)


    @property
    def iam_role(self):
        if self._iam_role is None:
            attach_policy_obj = json.loads(self.attach_policy)
            assume_policy_obj = json.loads(self.assume_policy)
            policy_been_modified = False

            try:
                self._iam_role = self.iam_client.get_role(RoleName=self.role_name)
            except botocore.exceptions.ClientError:
                # If a ClientError happened while getting the role, it means he do not exist.
                logging.debug(f"Creating {self.role_name} IAM Role..")

                self._iam_role = self.iam.create_role(
                    RoleName=self.role_name,
                    AssumeRolePolicyDocument=self.assume_policy
                )
                self.credentials_arn = self._iam_role.arn
                policy_been_modified = True

            # create or update the role's policies if needed
            policy = self.iam.RolePolicy(self.role_name, "inoft-vocal-permissions")
            try:
                if policy.policy_document != attach_policy_obj:
                    logging.debug(f"Updating inoft-vocal-permissions policy on {self.role_name} IAM Role.")
                    policy.put(PolicyDocument=self.attach_policy)
                    policy_been_modified = True

            except botocore.exceptions.ClientError:
                logging.debug(f"Creating inoft-vocal-permissions policy on {self.role_name} IAM Role.")
                policy.put(PolicyDocument=self.attach_policy)
                policy_been_modified = True

            if self.iam_role.assume_role_policy_document != assume_policy_obj:
                if (set(self.iam_role.assume_role_policy_document['Statement'][0]['Principal']['Service'])
                        != set(assume_policy_obj['Statement'][0]['Principal']['Service'])):

                    logging.debug(f"Updating assume role policy on {self.role_name} IAM Role.")
                    self.iam_client.update_assume_role_policy(
                        RoleName=self.role_name,
                        PolicyDocument=self.assume_policy
                    )
                    policy_been_modified = True

        return self._iam_role

    @iam_role.setter
    def iam_role(self, iam_role) -> None:
        self._iam_role = iam_role

    @property
    def credentials_arn(self):
        if self._credentials_arn is None:
            self._credentials_arn = self.iam_role.arn
        return self._credentials_arn

    @credentials_arn.setter
    def credentials_arn(self, credentials_arn) -> None:
        self._credentials_arn = credentials_arn

    def create_s3_bucket_if_missing(self, bucket_name: str, region_name: str):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            available_regions_for_s3 = boto3.Session().get_available_regions(service_name="s3")
            if region_name not in available_regions_for_s3:
                raise Exception(f"The region {region_name} was not available for s3. Here is the available regions : {available_regions_for_s3}")

            self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                "LocationConstraint": region_name
            })
            click.echo(f"Completed creation of new bucket ({bucket_name}) in region {region_name}")

    def upload_to_s3(self, filepath: str, bucket_name: str, region_name: str) -> bool:
        # If an error happen while uploading to S3, then the upload will not be
        # successful. We use that as our way to send a success response.
        try:
            self.create_s3_bucket_if_missing(bucket_name=bucket_name, region_name=region_name)
            self.s3_client.upload_file(Filename=filepath, Bucket=bucket_name, Key=Path(filepath).name)
            return True
        except Exception as e:
            print(f"Error while uploading to S3 : {e}")
            return False

if __name__ == "__main__":
    Core().upload_to_s3("F:\Inoft\hackaton cite des sciences 1\lambda_project\inoft_vocal_framework\cli\core\core_clients.py",
                        "letestduframeworkinoft", "eu-west-3")
