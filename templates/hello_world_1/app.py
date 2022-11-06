from inoft_vocal_framework import InoftSkill, InoftRequestHandler, InoftStateHandler, InoftDefaultFallback
import os


class LaunchRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self):
        self.say(MSGS_WELCOME.pick())
        self.persistent_memorize("hasLaunchedOnce", True)
        return self.to_platform_dict()

class LaunchStateHandler(InoftStateHandler):
    def handle(self):
        if YesHandler(self).can_handle():
            self.say("The user said yes !")
            return self.to_platform_dict()

        elif NoHandler(self).can_handle():
            self.say("Why did you said no ?")
            return self.to_platform_dict()

    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class YesHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["AMAZON.YesIntent", "OkConfirmation"])

    def handle(self):
        self.say(f"Why did you said Yes even if you are not in a state handler ?")
        return self.to_platform_dict()

class NoHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["AMAZON.NoIntent"])

    def handle(self):
        self.say(f"Why did you said No even if you are not in a state handler ?")
        return self.to_platform_dict()

class DefaultFallback(InoftDefaultFallback):
    def handle(self):
        self.say("I have no idea what you want to say")
        return self.to_platform_dict()


def lambda_handler(event, context):
    skill_builder = InoftSkill(settings_yaml_filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.yaml"))
    skill_builder.add_request_handler(LaunchRequestHandler)
    skill_builder.add_request_handler(YesHandler)
    skill_builder.add_request_handler(NoHandler)
    skill_builder.add_state_handler(LaunchStateHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)

if __name__ == "__main__":
    from inoft_vocal_framework import Simulator
    event_, context_ = Simulator(event_type="google-assistant-v1_start-request").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event_, context=context_)}")

