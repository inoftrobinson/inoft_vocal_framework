import time
from asyncio import Future
from concurrent.futures.thread import ThreadPoolExecutor
import boto3
from typing import List

from inoft_vocal_engine.inoft_vocal_framework.cli import ATTACH_POLICY, ASSUME_POLICY


class AwsCoreClients:
    CLIENT_BOTO_SESSION = 10000
    CLIENT_S3 = 10001
    CLIENT_DYNAMODB = 10002
    CLIENT_LAMBDA = 10003
    CLIENT_API_GATEWAY = 10004
    CLIENT_EVENTS = 10005
    CLIENT_IAM = 10006
    RESOURCE_IAM = 10007

    def __init__(self, clients_to_load: List[int]):
        self._boto_session, self._s3_client, self._lambda_client, self._dynamodb_client, self._api_gateway_client, \
        self._events_client, self._iam_client, self._iam_resource = None, None, None, None, None, None, None, None

        self.attach_policy = ATTACH_POLICY
        self.assume_policy = ASSUME_POLICY

        self.pool = ThreadPoolExecutor(len(clients_to_load))
        # We cannot use asyncio for the initialization of the client, because currently the http
        # requests made by boto3 are blocking http request made with the default urllib library.
        # See (https://www.mathewmarcus.com/blog/asynchronous-aws-api-requests-with-asyncio.html)

        futures: List[Future] = list()
        if self.CLIENT_BOTO_SESSION in clients_to_load:
            futures.append(self.pool.submit(self._create_boto_session))
        if self.CLIENT_S3 in clients_to_load:
            futures.append(self.pool.submit(self._create_s3_client))
        if self.CLIENT_DYNAMODB in clients_to_load:
            futures.append(self.pool.submit(self._create_dynamodb_client))
        if self.CLIENT_LAMBDA in clients_to_load:
            futures.append(self.pool.submit(self._create_lambda_client))
        if self.CLIENT_API_GATEWAY in clients_to_load:
            futures.append(self.pool.submit(self._create_api_gateway_client))
        if self.CLIENT_EVENTS in clients_to_load:
            futures.append(self.pool.submit(self._create_events_client))
        if self.CLIENT_IAM in clients_to_load:
            futures.append(self.pool.submit(self._create_iam_client))
        if self.RESOURCE_IAM in clients_to_load:
            futures.append(self.pool.submit(self._create_iam_resource))

        for future in futures:
            while not future.done():
                time.sleep(0.01)

    def _raise_client_not_loaded(self, client_variable_name: str):
        raise Exception(f"{client_variable_name} was not in the clients_to_load list.")

    @property
    def boto_session(self) -> boto3.Session:
        if self._boto_session is None:
            self._raise_client_not_loaded("CLIENT_BOTO_SESSION")
        return self._boto_session
    
    def _create_boto_session(self):
        self._boto_session = boto3.Session()
        
    @property
    def s3_client(self) -> boto3.client:
        if self._s3_client is None:
            self._raise_client_not_loaded("CLIENT_S3")
        return self._s3_client

    def _create_s3_client(self):
        self._s3_client = boto3.client("s3")

    @property
    def dynamodb_client(self) -> boto3.client:
        if self._dynamodb_client is None:
            self._raise_client_not_loaded("CLIENT_DYNAMODB")
        return self._dynamodb_client

    def _create_dynamodb_client(self):
        self._dynamodb_client = boto3.client("dynamodb")
        
    @property
    def lambda_client(self) -> boto3.client:
        if self._lambda_client is None:
            self._raise_client_not_loaded("CLIENT_LAMBDA")
        return self._lambda_client

    def _create_lambda_client(self):
        self._lambda_client = boto3.client("lambda")

    @property
    def api_gateway_client(self) -> boto3.client:
        if self._api_gateway_client is None:
            self._raise_client_not_loaded("CLIENT_API_GATEWAY")
        return self._api_gateway_client

    def _create_api_gateway_client(self):
        self._api_gateway_client = boto3.client("apigatewayv2")
        
    @property
    def events_client(self) -> boto3.client:
        if self._events_client is None:
            self._raise_client_not_loaded("CLIENT_EVENTS")
        return self._events_client

    def _create_events_client(self):
        self._events_client = boto3.client("events")
        
    @property
    def iam_client(self) -> boto3.client:
        if self._iam_client is None:
            self._raise_client_not_loaded("CLIENT_IAM")
        return self._iam_client

    def _create_iam_client(self):
        self._iam_client = boto3.client("iam")
        # todo: check if the iam from the boto_session is equivalent to the classical iam_client
        
    @property
    def iam_resource(self) -> boto3.client:
        if self._iam_resource is None:
            self._raise_client_not_loaded("RESOURCE_IAM")
        return self._iam_resource

    def _create_iam_resource(self):
        self._iam_resource = boto3.resource("iam")
