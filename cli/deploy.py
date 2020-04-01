import inspect
import os
import zipfile
from pathlib import Path

import boto3
import botocore
import click
from botocore.exceptions import ClientError
from click import ClickException

from inoft_vocal_framework.cli.cli_cache import CliCache
from inoft_vocal_framework.cli.core.core import Core
from inoft_vocal_framework.skill_builder.skill_settings import Settings


class DeployHandler(Core):
    def __init__(self):
        super().__init__()

    def handle(self):
        changed_root_folderpath = False
        app_project_root_folderpath = CliCache.cache().get("appProjectRootFolderpath").to_str(default=None)

        def prompt_user_to_select_folderpath():
            return click.prompt(text="What is the root folder path of your project ? "
                                     "This is the default if you do not write anything :",
                                default=str(Path(os.path.dirname(os.path.abspath(__file__))).parents[1]))


        if app_project_root_folderpath is None:
            app_project_root_folderpath = prompt_user_to_select_folderpath()
            changed_root_folderpath = True
        while not os.path.exists(app_project_root_folderpath):
            if click.confirm(text="The root folder path of the project has not been found."
                                  "Do you want to select a new folderpath ? Otherwise the CLI will close."):
                app_project_root_folderpath = prompt_user_to_select_folderpath()
                changed_root_folderpath = True
            else:
                exit(200)

        if changed_root_folderpath is True:
            CliCache.cache().put("appProjectRootFolderpath", app_project_root_folderpath)

        bucket_name = CliCache.cache().get("s3BucketName").to_str(default=None)
        if bucket_name is None:
            bucket_name = click.prompt("What will be your S3 bucket name to host your deployment files ?", type=str)
            CliCache.cache().put("s3BucketName", bucket_name)

        lambda_name = CliCache.cache().get("lambdaName").to_str(default=None)
        if lambda_name is None:
            lambda_name = click.prompt("What will be your Lambda (which act as the 'server' for your app) name ?", type=str)
            CliCache.cache().put("lambdaName", lambda_name)

        # todo: ask and check lambda handler file/function path

        CliCache.save_cache_to_yaml()


        DeployHandler().deploy(
            app_project_root_folderpath=app_project_root_folderpath,
            bucket_name=bucket_name,
            lambda_name=lambda_name,
            lambda_handler="app.lambda_handler",
            upload_zip=True,
        )

    def deploy(self, app_project_root_folderpath: str, bucket_name: str, lambda_name: str, lambda_handler: str,
               upload_zip: bool = True, app_project_existing_zip_filepath: str = None,
               lambda_description: str = "Inoft Vocal Framework Deployment",
               lambda_timeout_seconds=30, lambda_memory_size=512, publish=True, runtime="python3.7"):

        self.settings.find_load_settings_file(root_folderpath=app_project_root_folderpath)

        # Make sure this isn't already deployed.
        """deployed_versions = self.get_lambda_function_versions(lambda_name)
        if len(deployed_versions) > 0:
            print(f"This lambda function for this application is {click.style('already deployed', fg='green')}" +
                  f" If some part of the full deployment failed or you changed some resource name, and you want to do it again, type Y."
                  f" Otherwise, use the {click.style('inoft update', bold=True)} command")
            if not click.confirm("Do you want to redo the deployment ?"):
                print(f"Ok ! Remember to use the {click.style('inoft update', bold=True)} command !")
                exit()
        """

        zip_filepath, upload_success = None, None
        if upload_zip is True:
            if app_project_existing_zip_filepath is None:
                # Create the Lambda Zip
                zip_filepath = self.create_package(app_folder_path=app_project_root_folderpath)
                # todo: do not include any venv or sam folder when deploying
            else:
                if not os.path.isfile(app_project_existing_zip_filepath):
                    raise Exception(f"Existing app project zip file do not exist at filepath : {app_project_existing_zip_filepath}")
                zip_filepath = app_project_existing_zip_filepath

            # Upload it to S3
            click.echo("Uploading the app zip file to S3")
            upload_success = self.upload_to_s3(filepath=zip_filepath, object_key_name=Path(zip_filepath).name,
                                               bucket_name=bucket_name, region_name="eu-west-3")
            if not upload_success:
                raise ClickException("Unable to upload to S3. Quitting.")
            click.echo("Uploading completed.")

        try:
            lambda_arn = self.get_lambda_function_arn(function_name=lambda_name)
            print(f"Using the existing lambda function {lambda_name}")
            if upload_success is True:
                self.update_lambda_function_code(lambda_arn=lambda_arn, object_key_name=Path(zip_filepath).name, bucket_name=bucket_name)
                click.echo(f"Updated the code of the lambda with arn {lambda_arn}")

        except botocore.exceptions.ClientError:
            try:
                lambda_arn = self.create_lambda_function(bucket=bucket_name, s3_key=Path(zip_filepath).name, function_name=lambda_name,
                                                         handler=lambda_handler, description=lambda_description,
                                                         timeout=lambda_timeout_seconds, memory_size=lambda_memory_size,
                                                         runtime=runtime, publish=publish)
                print(f"Created the lambda function : {lambda_name}")
            except Exception as e:
                print(f"Error while updating the function by giving it a S3 path. Trying to update the"
                      f"function with a byte_stream of the zip file of the deployment package : {e}")

                with open(zip_filepath, mode="rb") as file_stream:
                    byte_stream = file_stream.read()

                lambda_arn = self.create_lambda_function(local_zip=byte_stream, function_name=lambda_name,
                                                         handler=lambda_handler, description=lambda_description,
                                                         timeout=lambda_timeout_seconds, memory_size=lambda_memory_size,
                                                         runtime=runtime, publish=publish)
                print(f"Created the lambda function : {lambda_name}")

        # Create and configure the API Gateway
        need_to_create_api = False
        api_gateway_id = self.settings.settings.get("deployment").get("api_gateway_id").to_str(default=None)
        if api_gateway_id is None or self.api_gateway_v2_exist(api_gateway_id) is False:
            api_id = self.create_api_gateway(lambda_arn=lambda_arn, lambda_name=lambda_name)
            print(f"Created a new {click.style(text='API Gateway', bold=True)}")
            self.settings.settings.get("deployment").put("api_gateway_id", api_id)
            self.settings.save_settings()
        else:
            print(f"Using the existing ApiGatewayV2 with id {click.style(text=api_gateway_id, bold=True, fg='green')}")

        return True

        # Remove the project zip from S3.
        if not source_zip:
            self.remove_uploaded_zip()


    @staticmethod
    def create_package(app_folder_path: str) -> str:
        archive_destination_filepath = os.path.join(Path(app_folder_path).parent, f"{Path(app_folder_path).name}.zip")
        click.echo(f"Making an archive from all the files and folders in {app_folder_path} to {archive_destination_filepath}")

        folders_names_to_excludes = [".aws-sam", ".idea", "__pycache__", "venv"]

        # Create a ZipFile Object
        with zipfile.ZipFile(archive_destination_filepath, "w") as zip_object:
            for root_dirpath, dirs, filenames in os.walk(app_folder_path, topdown=True):
                # The topdown arg allow use to modify the dirs list in the walk, and so we can easily exclude folders.
                dirs[:] = [dirpath for dirpath in dirs if Path(dirpath).name not in folders_names_to_excludes]

                relative_root_dirpath = root_dirpath.replace(app_folder_path, "")
                for filename in filenames:
                    zip_object.write(filename=os.path.join(root_dirpath, filename),
                                     arcname=os.path.join(relative_root_dirpath, filename))

        # from shutil import make_archive
        # zip_filepath = make_archive(base_name=archive_destination_filepath_without_extension, format="zip", root_dir=app_folder_path)
        print(f"Archive completed at {click.style(text=archive_destination_filepath, bold=True)}")

        # Warn if this is too large for Lambda.
        file_stats = os.stat(archive_destination_filepath)
        if file_stats.st_size > 52428800:
            click.echo("Warning: Application zip package is likely to be too large for AWS Lambda. Try to make it smaller")

        return archive_destination_filepath


if __name__ == "__main__":
    DeployHandler().handle()
