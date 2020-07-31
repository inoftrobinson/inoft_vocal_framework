from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type


class Endpoints:
    def __init__(self, alexa_api_endpoint_url_not_recommended_to_use: str = None,
                 google_assistant_api_endpoint_url: str = None, samsung_bixy_api_endpoint_url: str = None,
                 siri_api_endpoint_url: str = None):
        self.alexa_api_endpoint_url_not_recommended_to_use = None
        self.googleAssistantApiEndointUrl = None
        self.samsungBixbyApiEndointUrl = None
        self.siriApiEndointUrl = None


class Deployment:
    def __init__(self, handler_function_path: str, api_gateway_id: str, s3_bucket_name: str, lambda_name: str,
                 endpoints: Endpoints):
        self.handler_function_path = handler_function_path
        self.api_gateway_id = api_gateway_id
        self.s3_bucket_name = s3_bucket_name
        self.lambda_name = lambda_name
        self.endpoints = endpoints

    @property
    def handler_function_path(self) -> str:
        return self._handler_function_path

    @handler_function_path.setter
    def handler_function_path(self, handler_function_path: str) -> None:
        raise_if_variable_not_expected_type(value=handler_function_path, expected_type=str,
                                            variable_name="handler_function_path")
        self._handler_function_path = handler_function_path

    @property
    def api_gateway_id(self) -> str:
        return self._api_gateway_id

    @api_gateway_id.setter
    def api_gateway_id(self, api_gateway_id: str) -> None:
        raise_if_variable_not_expected_type(value=api_gateway_id, expected_type=str, variable_name="api_gateway_id")
        self._api_gateway_id = api_gateway_id

    @property
    def s3_bucket_name(self) -> str:
        return self._s3_bucket_name

    @s3_bucket_name.setter
    def s3_bucket_name(self, s3_bucket_name: str) -> None:
        raise_if_variable_not_expected_type(value=s3_bucket_name, expected_type=str, variable_name="s3_bucket_name")
        self._s3_bucket_name = s3_bucket_name

    @property
    def lambda_name(self) -> str:
        return self._lambda_name

    @lambda_name.setter
    def lambda_name(self, lambda_name: str) -> None:
        raise_if_variable_not_expected_type(value=lambda_name, expected_type=str, variable_name="lambda_name")
        self._lambda_name = lambda_name

    @property
    def endpoints(self) -> Endpoints:
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints: Endpoints) -> None:
        raise_if_variable_not_expected_type(value=endpoints, expected_type=self.Endpoints, variable_name="endpoints")
        self._endpoints = endpoints