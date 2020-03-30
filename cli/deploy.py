import inspect
import os
import zipfile
from pathlib import Path

import boto3
import botocore
import click
from botocore.exceptions import ClientError
from click import ClickException

from inoft_vocal_framework.cli.core.core import Core

class CliHandlers(Core):
    def __init__(self):
        super().__init__()
        self._lambda_name = None
        self._s3_bucket_name = None
        self.lambda_function = None

        self.use_apigateway = True
        # Do not change it, the framework only support api gateway as of today.

    @property
    def lambda_name(self) -> str:
        if self._lambda_name is None:
            self._lambda_name = "test"  # todo: make dynamic
        return self._lambda_name

    @property
    def s3_bucket_name(self) -> str:
        if self._s3_bucket_name is None:
            self._s3_bucket_name = "letestduframeworkinoft"  # todo: make dynamic
        return self._s3_bucket_name

    def deploy(self, app_project_folderpath: str, bucket_name: str, lambda_name: str, lambda_handler: str,
               create_and_upload_new_zip: bool = True, app_project_existing_zip_filepath: str = None,
               lambda_description: str = "Inoft Vocal Framework Deployment",
               lambda_timeout_seconds=30, lambda_memory_size=512, publish=True, runtime="python3.7"):

        # Make sure this isn't already deployed.
        deployed_versions = self.get_lambda_function_versions(self.lambda_name)
        if len(deployed_versions) > 0:
            raise ClickException("This application is " + click.style("already deployed", fg="red") +
                                 " - did you mean to call " + click.style("update", bold=True) + "?")

        if create_and_upload_new_zip is True:
            # Create the Lambda Zip
            zip_filepath = self.create_package(app_folder_path=app_project_folderpath)

            # Upload it to S3
            click.echo("Uploading the app zip file to S3")
            upload_success = self.upload_to_s3(filepath=zip_filepath, bucket_name=self.s3_bucket_name, region_name="eu-west-3")
            if not upload_success:
                raise ClickException("Unable to upload to S3. Quitting.")
            click.echo("Uploading completed.")
        elif app_project_existing_zip_filepath is not None:
            if not os.path.isfile(app_project_existing_zip_filepath):
                raise Exception(f"No file has been found at {app_project_existing_zip_filepath}")
            zip_filepath = app_project_existing_zip_filepath
        else:
            raise Exception(f"If you do not with to create and upload a new zip file, please specify the path of an existing zip file.")

        # Fixes https://github.com/Miserlou/Zappa/issues/613
        try:
            self.lambda_function = self.get_lambda_function(function_name=lambda_name)
        except botocore.exceptions.ClientError:
            # Register the Lambda function with that zip as the source
            # You'll also need to define the path to your lambda_handler code.
            with open(zip_filepath, mode="rb") as file_stream:
                byte_stream = file_stream.read()

            kwargs = dict(
                bucket=bucket_name,
                s3_key=Path(zip_filepath).name,
                function_name=lambda_name,
                handler=lambda_handler,
                description=lambda_description,
                timeout=lambda_timeout_seconds,
                memory_size=lambda_memory_size,
                runtime=runtime,
                publish=publish,
                local_zip=byte_stream,
            )
            self.lambda_function = self.create_lambda_function(**kwargs)

        # Schedule events for this deployment
        # self.schedule()

        endpoint_url = ''
        deployment_string = click.style("Deployment complete", fg="green", bold=True) + "!"

        if self.use_apigateway:
            # Create and configure the API Gateway
            template = self.create_stack_template(
                lambda_arn=self.lambda_arn,
                lambda_name=self.lambda_name,
                api_key_required=self.api_key_required,
                iam_authorization=self.iam_authorization,
                authorizer=self.authorizer,
                cors_options=self.cors,
                description=self.apigateway_description,
                endpoint_configuration=self.endpoint_configuration
            )

            self.zappa.update_stack(
                self.lambda_name,
                self.s3_bucket_name,
                wait=True,
                disable_progress=self.disable_progress
            )

            api_id = self.zappa.get_api_id(self.lambda_name)

            # Add binary support
            if self.binary_support:
                self.zappa.add_binary_support(api_id=api_id, cors=self.cors)

            # Add payload compression
            if self.stage_config.get('payload_compression', True):
                self.zappa.add_api_compression(
                    api_id=api_id,
                    min_compression_size=self.stage_config.get('payload_minimum_compression_size', 0))

            # Deploy the API!
            endpoint_url = self.deploy_api_gateway(api_id)
            deployment_string = deployment_string + ": {}".format(endpoint_url)

            # Create/link API key
            if self.api_key_required:
                if self.api_key is None:
                    self.zappa.create_api_key(api_id=api_id, stage_name=self.api_stage)
                else:
                    self.zappa.add_api_stage_to_api_key(api_key=self.api_key, api_id=api_id, stage_name=self.api_stage)

            if self.stage_config.get('touch', True):
                self.touch_endpoint(endpoint_url)

        # Finally, delete the local copy our zip package
        if not source_zip:
            if self.stage_config.get('delete_local_zip', True):
                self.remove_local_zip()

        # Remove the project zip from S3.
        if not source_zip:
            self.remove_uploaded_zip()

        click.echo(deployment_string)

    @staticmethod
    def create_package(app_folder_path: str) -> str:
        archive_destination_filepath_without_extension = os.path.join(Path(app_folder_path).parent, Path(app_folder_path).name)
        click.echo(f"Making an archive from all the files and folders in {app_folder_path} to {archive_destination_filepath_without_extension}.zip")

        from shutil import make_archive
        zip_filepath = make_archive(base_name=archive_destination_filepath_without_extension, format="zip", root_dir=app_folder_path)
        click.echo(f"Archive completed at {zip_filepath}")

        # Warn if this is too large for Lambda.
        file_stats = os.stat(zip_filepath)
        if file_stats.st_size > 52428800:
            click.echo("Warning: Application zip package is likely to be too large for AWS Lambda. Try to make it smaller")

        return zip_filepath

CliHandlers().deploy(
    app_project_folderpath="F:\Inoft\hackaton cite des sciences 1\lambda_project",
    bucket_name="letestduframeworkinoft",
    lambda_name="lambda_functionelambda_handler",
    lambda_handler="app.lambda_handler",
    create_and_upload_new_zip=False,
    app_project_existing_zip_filepath="F:\Inoft\hackaton cite des sciences 1\lambda_project.zip",
)
