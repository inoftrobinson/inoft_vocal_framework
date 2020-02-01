from inoft_vocal_framework.utils import get_dict_of_all_custom_defined_variables_of_class


class RefsAvailablePlatforms:
    REF_PLATFORM_ALEXA_V1 = 0
    REF_PLATFORM_GOOGLE_ASSISTANT_V1 = 1

    @staticmethod
    def get_all_available_platforms_refs() -> dict:
        return get_dict_of_all_custom_defined_variables_of_class(RefsAvailablePlatforms)

class CurrentPlatformData:
    used_platform_id = None

    @staticmethod
    def set_used_platform_id(platform_ref: int) -> None:
        available_platforms_refs = RefsAvailablePlatforms.get_all_available_platforms_refs()
        for key_platform_ref, value_platform_ref in available_platforms_refs.items():
            # We check that the selected platform ref is an available ref. We do not use the in keyword on
            # the values of the dict, because we want to print the key of the platform that is being used.
            if platform_ref == value_platform_ref:
                CurrentPlatformData.used_platform_id = platform_ref
                print(f"{key_platform_ref} platform is being used.")
                return None

        raise Exception(f"The platform_ref {platform_ref} is not a valid ref. Here is all the available refs : {available_platforms_refs}")

