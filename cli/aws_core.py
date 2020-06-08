import time
from concurrent.futures.thread import ThreadPoolExecutor

import boto3
import botocore
import click
from botocore.exceptions import ClientError, NoCredentialsError


class AwsCore:
    CLIENT_BOTO_SESSION = "boto_session"
    CLIENT_S3 = "s3"

    def __init__(self, clients_to_load: list = [CLIENT_BOTO_SESSION, CLIENT_S3]):
        self.boto_session = None
        self.s3_client = None

        self.pool = ThreadPoolExecutor(len(clients_to_load))
        # We cannot use asyncio for the initialization of the client, because currently the http
        # requests made by boto3 are blocking http request made with the default urllib library.
        # See (https://www.mathewmarcus.com/blog/asynchronous-aws-api-requests-with-asyncio.html)

        futures = list()
        if self.CLIENT_BOTO_SESSION in clients_to_load:
            boto_session_future = self.pool.submit(self._create_boto_session)
            futures.append(boto_session_future)
        if self.CLIENT_S3 in clients_to_load:
            s3_client_future = self.pool.submit(self._create_s3_client)
            futures.append(s3_client_future)

        for future in futures:
            while not future.done():
                time.sleep(0.01)

    def _create_boto_session(self):
        self.boto_session = boto3.Session()

    def _create_s3_client(self):
        self.s3_client = boto3.client("s3")

    def create_s3_bucket_if_missing(self, bucket_name: str, region_name: str):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            click.echo(f"Trying to create a new S3 Bucket with name {click.style(text=bucket_name, fg='yellow', bold=True)}"
                       f" in region {click.style(text=region_name, fg='yellow', bold=True)}")
            available_regions_for_s3 = self.boto_session.get_available_regions(service_name="s3")
            if region_name not in available_regions_for_s3:
                raise Exception(f"The region {region_name} was not available for s3. Here is the available regions : {available_regions_for_s3}")

            self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region_name})
            click.echo(f"Completed creation of the new bucket.")

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


    def remove_from_s3(self, file_name: str, bucket_name: str):
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
