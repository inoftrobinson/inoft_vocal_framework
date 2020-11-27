import os
from inoft_vocal_engine import InoftSkill, InoftCondition, InoftRequestHandler, InoftStateHandler, InoftDefaultFallback


class YesCondition(InoftCondition):
    def can_handle(self) -> bool:
        return self.is_in_intent_names(["AMAZON.YesIntent", "YesIntent"])


class StartRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self) -> dict:
        self.say("Hey ! Are you ready for your first fact about the Inoft Vocal Framework ?")
        self.memorize_session_then_state(SayFactOnYesStateHandler)
        return self.to_platform_dict()


class GetFactRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_in_intent_names("GetFact")

    def handle(self) -> dict:
        from messages import MSGS_START_FACT, MSGS_END_FACT, MSGS_FACTS, MSGS_NEW_FACT
        self.say(f"{MSGS_START_FACT.pick()} {MSGS_FACTS.pick()} {MSGS_END_FACT.pick()} {MSGS_NEW_FACT.pick()}")
        self.memorize_session_then_state(SayFactOnYesStateHandler)
        return self.to_platform_dict()


class SayFactOnYesStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            return GetFactRequestHandler(self).handle()
        else:
            self.say("I'm supposed to be here to give you facts. Yet if i want i can give you some infos about this application. What do you say ? Yes ?")
            return self.to_platform_dict()


class GetFactOrCloseStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesCondition(self).can_handle():
            return GetFactRequestHandler(self).handle()
        else:
            self.say("Oki ! Have a great day !")
            self.end_session()
            return self.to_platform_dict()


class WantSomeInformationsStateHandler(InoftStateHandler):
    def handle(self):
        if YesCondition(self).can_handle():
            self.say(f"The application to thank for us talking to each other, has been developed in Python with the Inoft Vocal Framework, "
                     f"and work both for me {'Alexa, and also Google Assistant' if self.is_alexa else 'Google Assistant, and also Alexa'}")
        else:
            self.say("Then if you do not want a fact, i'm going to close myself. So, do you want a fact ?")
        return self.to_platform_dict()


class DefaultFallback(InoftDefaultFallback):
    def handle(self):
        self.say("I did not followed you on that one. Would like me to tell you a fact about the Inoft Vocal Framework ?")
        self.memorize_session_then_state(SayFactOnYesStateHandler)
        return self.to_platform_dict()


def lambda_handler(event, context):
    skill_builder = InoftSkill(settings_yaml_filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.yaml"))
    skill_builder.add_request_handler(StartRequestHandler)
    skill_builder.add_request_handler(GetFactRequestHandler)
    skill_builder.add_state_handler(SayFactOnYesStateHandler)
    skill_builder.add_state_handler(GetFactOrCloseStateHandler)
    skill_builder.add_state_handler(WantSomeInformationsStateHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)

if __name__ == "__main__":
    from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.simulator import Simulator
    event_, context_ = Simulator(event_type="alexa/start").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event_, context=context_)}")
