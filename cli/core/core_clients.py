import boto3
from inoft_vocal_framework.cli.core.policies import ATTACH_POLICY, ASSUME_POLICY


class CoreClients:
    def __init__(self):
        self.attach_policy = ATTACH_POLICY
        self.assume_policy = ASSUME_POLICY

        self._boto_session = None

        self._lambda_client = None
        self._s3_client = None
        self._dynamodb_client = None
        self._api_gateway_client = None
        self._events_client = None

        east_config = boto3.session.Config(region_name="us-east-1")
        self.acm_client = boto3.client("acm", config=east_config)
        self.iam_client = boto3.client("iam")
        self.iam_resource = boto3.resource("iam")
        self.iam = self.boto_session.client("iam")
        self.cloudformation_client = boto3.client("cloudformation")
        self.cloudwatch = boto3.client("cloudwatch")

    @property
    def boto_session(self):
        if self._boto_session is None:
            self._boto_session = boto3.Session()
        return self._boto_session

    @property
    def lambda_client(self):
        if self._lambda_client is None:
            self._lambda_client = boto3.client("lambda")
        return self._lambda_client

    @property
    def s3_client(self):
        if self._s3_client is None:
            self._s3_client = boto3.client("s3")
        return self._s3_client

    @property
    def dynamodb_client(self):
        if self._dynamodb_client is None:
            self._dynamodb_client = boto3.client("dynamodb")
        return self._dynamodb_client

    @property
    def api_gateway_client(self):
        if self._api_gateway_client is None:
            self._api_gateway_client = boto3.client("apigatewayv2")
        return self._api_gateway_client

    @property
    def events_client(self):
        if self._events_client is None:
            self._events_client = boto3.client("events")
        return self._events_client
