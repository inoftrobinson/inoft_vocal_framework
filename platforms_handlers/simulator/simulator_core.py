import os
from json import load as json_load
from typing import Optional

from inoft_vocal_framework.utils.general import load_json


class Simulator:
    PLATFORM_ALEXA = "alexa"
    PLATFORM_GOOGLE = "google"
    PLATFORM_BIXBY = "bixby"
    AVAILABLE_PLATFORMS = [PLATFORM_ALEXA, PLATFORM_GOOGLE, PLATFORM_BIXBY]

    def __init__(self, event_type: str, platform: Optional[str] = None, is_event_with_wrapper: Optional[bool] = False):
        self.platform = platform
        self.is_event_with_wrapper = is_event_with_wrapper

        self.current_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.wrappers_folderpath = os.path.join(self.current_dir_path, "wrappers")
        self.request_samples_folderpath = os.path.join(self.current_dir_path, "request_samples")
        self.event_file_filepath = os.path.join(self.request_samples_folderpath, "" if platform is None else platform, f"{event_type}.json")
        if not os.path.isfile(self.event_file_filepath):
            raise Exception(f"No event file was found at {self.event_file_filepath}. Please use a valid event_type name.")

    def get_event_and_context(self) -> (str, str):
        event = None
        context = None

        if self.is_event_with_wrapper is False:
            event_body = load_json(self.event_file_filepath)

            if self.platform not in self.AVAILABLE_PLATFORMS:
                raise Exception(f"The platform named {self.platform} has not been found in the available platforms : {self.AVAILABLE_PLATFORMS}")

            if self.platform == self.PLATFORM_GOOGLE:
                event = load_json(os.path.join(self.wrappers_folderpath, "api_gateway_google_path_wrapper.json"))
                event["body"] = event_body
            elif self.platform == self.PLATFORM_ALEXA:
                event = event_body
            elif self.platform == self.PLATFORM_BIXBY:
                pass
        else:
            event = load_json(self.event_file_filepath)

        return event, context
