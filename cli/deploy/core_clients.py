from concurrent.futures import ThreadPoolExecutor
import time
import boto3
from inoft_vocal_framework.cli.deploy.policies import ATTACH_POLICY, ASSUME_POLICY


class CoreClients:
    def __init__(self):  #, pool: ThreadPoolExecutor):
        self.attach_policy = ATTACH_POLICY
        self.assume_policy = ASSUME_POLICY

        self.boto_session = None
        self.lambda_client = None
        self.s3_client = None
        self.dynamodb_client = None
        self.api_gateway_client = None
        self.events_client = None

        # east_config = boto3.session.Config(region_name="us-east-1")
        # self.acm_client = boto3.client("acm", config=east_config)
        self.iam_client = None
        self.iam_resource = None
        # self.iam = self.boto_session.client("iam")
        # self.cloudformation_client = boto3.client("cloudformation")
        # self.cloudwatch = boto3.client("cloudwatch")

        # self.pool = pool
        self.pool = ThreadPoolExecutor(8)
        # We cannot use asyncio for the initialization of the client, because currently the http
        # requests made by boto3 are blocking http request made with the default urllib library.
        # See (https://www.mathewmarcus.com/blog/asynchronous-aws-api-requests-with-asyncio.html)
        self.create_clients()

    def create_clients(self):
        boto_session_future = self.pool.submit(self._create_boto_session)
        lambda_client_future = self.pool.submit(self._create_lambda_client)
        s3_client_future = self.pool.submit(self._create_s3_client)
        dynamodb_client_future = self.pool.submit(self._create_dynamodb_client)
        api_gateway_client_future = self.pool.submit(self._create_api_gateway_client)
        events_client_future = self.pool.submit(self._create_events_client)
        iam_client_future = self.pool.submit(self._create_iam_client)
        iam_resource_future = self.pool.submit(self._create_iam_resource)
        while (not boto_session_future.done() or not lambda_client_future.done() or not s3_client_future.done() or not dynamodb_client_future.done()
               or not api_gateway_client_future.done() or not events_client_future.done() or not iam_client_future.done() or not iam_resource_future.done()):
            time.sleep(0.1)

    def _create_boto_session(self):
        self.boto_session = boto3.Session()

    def _create_lambda_client(self):
        self.lambda_client = boto3.client("lambda")

    def _create_s3_client(self):
        self.s3_client = boto3.client("s3")

    def _create_dynamodb_client(self):
        self.dynamodb_client = boto3.client("dynamodb")

    def _create_api_gateway_client(self):
        self.api_gateway_client = boto3.client("apigatewayv2")

    def _create_events_client(self):
        self.events_client = boto3.client("events")

    def _create_iam_client(self):
        self.iam_client = boto3.client("iam")
        self.iam = self.iam_client
        # todo: check if the iam from the boto_session is equivalent to the classical iam_client

    def _create_iam_resource(self):
        self.iam_resource = boto3.resource("iam")


if __name__ == "__main__":
    import time
    start_time = time.time()
    clients_instance = CoreClients()
    print(f"Initialization delay = {time.time() - start_time}")
    # print(clients_instance.iam_client.get_role(RoleName="InoftVocalFrameworkLambdaExecution")["Role"])
