import json
import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor

import boto3
import botocore
import click
from botocore.exceptions import ClientError, NoCredentialsError
from typing import List

from inoft_vocal_engine.cloud_providers.aws.core_clients import AwsCoreClients
from inoft_vocal_engine.safe_dict import SafeDict


class AwsCore(AwsCoreClients):
    def __init__(self, clients_to_load: List[int]):
        super().__init__(clients_to_load=clients_to_load)

        self.tags = {"framework": "InoftVocalFramework"}

        self._iam_role = None
        self._credentials_arn = None
        self._aws_account_id = None

        self._session_unix_time = None
        self._session_count_created_statement_ids = 0

        self.role_name = "InoftVocalFrameworkLambdaExecution"
        self.http_methods = ['ANY']

        self.default_description = "Created with the Inoft Vocal Framework"

    def create_s3_bucket_if_missing(self, bucket_name: str, region_name: str) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            click.echo(f"Trying to create a new S3 Bucket with name {click.style(text=bucket_name, fg='yellow', bold=True)}"
                       f" in region {click.style(text=region_name, fg='yellow', bold=True)}")
            available_regions_for_s3 = self.boto_session.get_available_regions(service_name="s3")
            if region_name not in available_regions_for_s3:
                raise Exception(f"The region {region_name} was not available for s3. Here is the available regions : {available_regions_for_s3}")

            self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region_name})
            click.echo(f"Completed creation of the new bucket.")
            return False

    def upload_to_s3(self, filepath: str, object_key_name: str, bucket_name: str, region_name: str) -> bool:
        # If an error happen while uploading to S3, then the upload will not be
        # successful. We use that as our way to send a success response.
        try:
            self.create_s3_bucket_if_missing(bucket_name=bucket_name, region_name=region_name)
            self.s3_client.upload_file(Filename=filepath, Bucket=bucket_name, Key=object_key_name)
            return True
        except NoCredentialsError as e:
            click.echo(f"Almost there ! You just need to configure your AWS credentials."
                       f"\nYou can follow the official documentation (you will need to install the awscli by running pip install awscli) "
                       f"then go to https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration")
        except Exception as e:
            click.echo(f"Error while getting/creating/uploading to the S3 bucket : {e}")
        return False

    def remove_from_s3(self, file_name: str, bucket_name: str) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                return False

        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
            return True
        except (botocore.exceptions.ParamValidationError, botocore.exceptions.ClientError):
            return False

    def get_lambda_function_arn(self, function_name: str) -> str or None:
        return SafeDict(self.lambda_client.get_function(FunctionName=function_name)).get("Configuration").get("FunctionArn").to_str(default=None)

    def api_gateway_v2_url(self, api_id: str) -> str or None:
        try:
            return SafeDict(self.api_gateway_client.get_api(ApiId=api_id)).get("ApiEndpoint").to_str(default=None)
        except Exception as e:
            return None

    def get_lambda_function_versions(self, function_name: str) -> list:
        try:
            response = self.lambda_client.list_versions_by_function(FunctionName=function_name)
            return response.get('Versions', list())
        except Exception as e:
            click.echo(f"Lambda function {function_name} not found. Error : {e}")
            return list()

    def create_lambda_function(self, bucket=None, s3_key: str = None, local_zip: bytes = None,
                               function_name: str = None, handler=None,
                               description: str = "Inoft Vocal Engine Deployment",
                               timeout: int = 30, memory_size: int = 512, publish: bool = True, runtime=None):
        """
        Given a bucket and key (or a local path) of a valid Lambda-zip, a function name and a handler, register that Lambda function.
        """
        kwargs = dict(
            FunctionName=function_name,
            Runtime=runtime,
            Role=self.credentials_arn,
            # "arn:aws:iam::631258222318:role/service-role/alexa_hackaton-cite-des-sciences_fakenews-challeng-role-ck3sxsyt",  # self.credentials_arn,
            # todo: make dynamic and create automaticly role if missing
            Handler=handler,
            Description=description,
            Timeout=timeout,
            MemorySize=memory_size,
            Publish=publish,
            Layers=[
                "arn:aws:lambda:eu-west-3:631258222318:layer:inoft-vocal-framework_v0-8dot3:2",
                "arn:aws:lambda:eu-west-3:631258222318:layer:ffmpeg:2",
            ]
            # Those ARNs point to the required lambda layers to use the framework. Please do not modify them.
        )
        if local_zip is not None:
            kwargs['Code'] = {
                'ZipFile': local_zip
            }
        else:
            kwargs['Code'] = {
                'S3Bucket': bucket,
                'S3Key': s3_key
            }

        response = self.lambda_client.create_function(**kwargs)

        lambda_arn = response["FunctionArn"]
        version = response['Version']

        click.echo(f"Created new lambda function {function_name} with arn of {lambda_arn}")
        return lambda_arn

    def update_lambda_function_code(self, lambda_arn: str, object_key_name: str, bucket_name: str) -> dict:
        response = self.lambda_client.update_function_code(
            FunctionName=lambda_arn,
            S3Bucket=bucket_name,
            S3Key=object_key_name,
            Publish=True,
        )
        return response

    def update_lambda_function_configuration(self, function_name: str, handler_function_path: str = None,
                                             lambda_layers_arns: list = None) -> dict:
        kwargs = dict(FunctionName=function_name)
        if handler_function_path is not None:
            kwargs["Handler"] = handler_function_path
        if lambda_layers_arns is not None and len(lambda_layers_arns) > 0:
            kwargs["Layers"] = lambda_layers_arns

        response = self.lambda_client.update_function_configuration(**kwargs)
        return response

    def create_api_gateway(self, lambda_arn: str, lambda_name: str, route_names: List[str], description: str = None) -> str or None:
        # todo: fix bug if id of api gateway is present in file, but the api has been deleted, it will not try to recreate it
        api_name = lambda_name or lambda_arn.split(":")[-1]

        api_creation_response = SafeDict(self.api_gateway_client.create_api(
            Name=api_name, Description=description or self.default_description, Target=lambda_arn, ProtocolType="HTTP"))
        api_id = api_creation_response.get("ApiId").to_str()

        self.create_and_setup_api_routes(api_id=api_id, lambda_arn=lambda_arn, route_names=route_names)
        return api_id

    def create_and_setup_api_routes(self, api_id: str, lambda_arn: str, route_names: List[str]):
        integration_creation_response = SafeDict(self.api_gateway_client.create_integration(
            ApiId=api_id, IntegrationType="AWS_PROXY", PayloadFormatVersion="2.0", IntegrationUri=lambda_arn, TimeoutInMillis=10000))

        integration_id = integration_creation_response.get("IntegrationId").to_str(default=None)
        if integration_id is None:
            raise Exception(
                f"Error while creating the route integration of the api towards the lambda_function."
                f"The integration_id was not found in the integration creation response."
                f"Please delete the api and redo the deployment."
                f"If the issue persist, create an Issue topic on the github page of the framework.")

        """route_names = ["amazonAlexaV1", "googleAssistantDialogflowV1", "samsungBixbyV1", "appleSiriV1"]
        route_names_to_settings_keys = {"amazonAlexaV1": "alexaApiEndpointUrlNotRecommendedToUse",
                                        "googleAssistantDialogflowV1": "googleAssistantApiEndointUrl",
                                        "samsungBixbyV1": "samsungBixbyApiEndointUrl",
                                        "appleSiriV1": "siriApiEndointUrl"}"""

        api_gateway_root_url = self.api_gateway_v2_url(api_id=api_id)
        for route_name in route_names:
            self.boto_session.get_credentials()
            response = self.api_gateway_client.create_route(
                ApiId=api_id,
                AuthorizationType="None",
                RouteKey=f"ANY /{route_name}",
                # A space is required between the HTTP method and the /
                Target=f"integrations/{integration_id}",
            )
            self.add_lambda_permission_to_call_api_resource(lambda_arn=lambda_arn, api_id=api_id, route_key=route_name)
            api_route_url = f"{api_gateway_root_url}/{route_name}"
            click.echo(f"Api route {click.style(route_name, fg='green')} creation complete accessible on {api_route_url}")
            # self.settings.get_set("deployment", {}).get_set("endpoints", {}).put(
            #    route_names_to_settings_keys[route_name], api_route_url).reset_navigated_dict()
            # We reset the navigated dict after a final put

    def add_lambda_permission_to_call_api_resource(self, lambda_arn: str, api_id: str, route_key: str):
        response = self.lambda_client.add_permission(
            FunctionName=lambda_arn,
            StatementId=self.get_session_new_statement_id(),
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
            SourceArn=f"arn:aws:execute-api:{self.boto_session.region_name}:{self.aws_account_id}:{api_id}/*/*/{route_key}",
        )

    @property
    def iam_role(self) -> SafeDict:
        if self._iam_role is None:
            try:
                self._iam_role = SafeDict(self.iam_client.get_role(RoleName=self.role_name)["Role"])
            except botocore.exceptions.ClientError:
                # If a ClientError happened while getting the role, it means he do not exist.
                logging.debug(f"Creating {self.role_name} IAM Role..")

                attach_policy_obj = json.loads(self.attach_policy)
                assume_policy_obj = json.loads(self.assume_policy)

                self._iam_role = SafeDict(self.iam_client.create_role(
                    RoleName=self.role_name, AssumeRolePolicyDocument=self.assume_policy)["Role"])

                # create or update the role's policies if needed
                policy = self.iam_resource.RolePolicy(self.role_name, "inoft-vocal-permissions")
                try:
                    if policy.policy_document != attach_policy_obj:
                        logging.debug(f"Updating inoft-vocal-permissions policy on {self.role_name} IAM Role.")
                        policy.put(PolicyDocument=self.attach_policy)

                except botocore.exceptions.ClientError:
                    logging.debug(f"Creating inoft-vocal-permissions policy on {self.role_name} IAM Role.")
                    policy.put(PolicyDocument=self.attach_policy)

                role_policy_dict = self._iam_role.get("AssumeRolePolicyDocument").to_dict()
                if role_policy_dict != assume_policy_obj:
                    if (SafeDict(role_policy_dict["Statement"][0]).get("Principal").get("Service").to_any()
                            != assume_policy_obj["Statement"][0]["Principal"]["Service"]):
                        logging.debug(f"Updating assume role policy on {self.role_name} IAM Role.")
                        self.iam_client.update_assume_role_policy(RoleName=self.role_name,
                                                                  PolicyDocument=self.assume_policy)

        return self._iam_role

    @property
    def credentials_arn(self):
        if self._credentials_arn is None:
            self._credentials_arn = self.iam_role.get("Arn").to_str()
        return self._credentials_arn

    @credentials_arn.setter
    def credentials_arn(self, credentials_arn) -> None:
        self._credentials_arn = credentials_arn

    @property
    def aws_account_id(self) -> str:
        if self._aws_account_id is None:
            self._aws_account_id = boto3.client("sts").get_caller_identity().get("Account")
        return self._aws_account_id

    def get_session_new_statement_id(self) -> str:
        # No restriction is set on the statement id. To created my type of ids, i take the same unix
        # time across the session, and each time we generated a new statement id, i add 1 to the unix time.
        # Dumb and simple, but it assure that i will never have the same id twice.
        if self._session_unix_time is None:
            self._session_unix_time = time.time()
        self._session_count_created_statement_ids += 1

        # After turning the modified unix time into a string, we remove any point, that would have
        # been used to  separate the decimals, because AWS cannot accept a point in a id string.
        return str(self._session_unix_time + self._session_count_created_statement_ids).replace(".", "")

if __name__ == "__main__":
    Core().upload_to_s3(
        "F:\Inoft\hackaton cite des sciences 1\lambda_project\inoft_vocal_engine\cli\core\core_clients.py",
        "letestduframeworkinoft", "eu-west-3")

