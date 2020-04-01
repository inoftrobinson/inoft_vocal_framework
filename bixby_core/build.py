"""""
function build(intent) {
    console.log(intent);

    let endpoints_json = {
        "action-endpoints": {
        }
    }
    endpoints_json["action-endpoints"].

    /*endpoints {
  action-endpoints {
    action-endpoint (launch) {
      accepted-inputs ($vivContext)
      // local-endpoint (launch.js)
      remote-endpoint ("{remote.url}") {
        method (POST)
      }
    }
    action-endpoint (ANumber) {
      accepted-inputs ($vivContext, IntNumber)
      local-endpoint (ANumber.js)
    }
    action-endpoint (GetContent) {
      accepted-inputs (searchTerm, $vivContext)
      local-endpoint (GetContent.js)
    }
  }
}*/
}"""""
from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type, raise_if_value_not_in_list

from inoft_vocal_framework.safe_dict import SafeDict

class ActionEndpoints:
    json_key = "action-endpoints"

    class NestedActionEndpoints:
        json_key = "action-endpoints"

        class RemoteEndpoint:
            json_key = "remote-endpoint"
            METHOD_GET = "GET"
            METHOD_PUT = "PUT"
            METHOD_POST = "POST"
            METHOD_DELETE = "DELETE"
            METHOD_UPDATE = "UPDATE"
            METHOD_OPTIONS = "OPTIONS"
            AVAILABLE_METHODS = [METHOD_GET, METHOD_PUT, METHOD_POST, METHOD_DELETE, METHOD_UPDATE, METHOD_OPTIONS]
            #todo: cannot use nested objects processing, need to use templating

            def __init__(self):
                self.method = None

        def __init__(self):
            self.accepted_inputs = None
            self.local_endpoint = None
            self._remote_endpoint = None

        @property
        def remote_endpoint(self):
            return self._remote_endpoint

        @remote_endpoint.setter
        def remote_endpoint(self, endpoint_url: str, endpoint_method: str = RemoteEndpoint.METHOD_POST) -> None:
            raise_if_variable_not_expected_type(value=endpoint_url, expected_type=endpoint_url, variable_name="endpoint_url")
            raise_if_value_not_in_list(value=endpoint_method, list_object=self.RemoteEndpoint.AVAILABLE_METHODS, variable_name="endpoint_method")
            self._remote_endpoint = self.RemoteEndpoint

        def return_transformations(self):
            vars(self)["accepted-inputs"] = self.accepted_inputs
            del self.accepted_inputs
            vars(self)["local-endpoint"] = self.local_endpoint
            del self.local_endpoint

    def __init__(self):
        self.action_endpoints = self.NestedActionEndpoints()


from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
endpoints = ActionEndpoints()
dict_object = NestedObjectToDict.get_dict_from_nested_object(object_to_process=ActionEndpoints(),
                                                             key_names_identifier_objects_to_go_into=["json_key"])
print(dict_object)

def build_endpoints():
    endpoints = SafeDict()
    endpoints.get_set("action-endpoints", dict()).get_set("action-endpoints")

# from inoft_vocal_framework.utils.general import load_json
# current_template_infos_dict = load_json(filepath="F:\Inoft\skill_histoire_decryptage\inoft_vocal_framework\bixby_core\dummy_test.json")

