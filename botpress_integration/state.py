from inoft_vocal_framework import InoftSkill, InoftRequestHandler, InoftStateHandler, InoftDefaultFallback
from messages import *
import os


class NodeLeostorystartRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self) -> dict:
        self.say(BUILTIN_TEXT_DJKP2N.pick())
        self.memorize_session_then_state(NodeLeostorystartStateHandler)
        return self.to_platform_dict()

class NodeLeostorystartStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesHandler(self).can_handle():
            self.say(BUILTIN_TEXT_LBS0RE.pick())
            self.memorize_session_then_state(NodeDfcTwoStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class TopicChoicesStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if GenericHandler(self).can_handle():
            self.memorize_session_then_state(Contexts.flow.jsonStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(Memory.flow.jsonStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(CatchStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class CatchStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiftySevenFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeTwoSeventyNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDebOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeTwoSeventyNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFaFiftyOneStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if Yes_chefHandler(self).can_handle():
            self.say(BUILTIN_TEXT_MVDSF5.pick())
            self.memorize_session_then_state(NodeEdafStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeDFivehundredandeightyNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeTwoSeventyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesHandler(self).can_handle():
            self.say(BUILTIN_TEXT_NIVD2C.pick())
            self.memorize_session_then_state(NodeDEightFiveStateHandler)
            return self.to_platform_dict()
        
        elif NoHandler(self).can_handle():
            self.say(BUILTIN_TEXT_GZ5LMT.pick())
            self.memorize_session_then_state(NodeFaFiftyOneStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeDbdaStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFSixtyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeTwoSeventyNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDEightFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if Yes_chefHandler(self).can_handle():
            self.say(BUILTIN_TEXT_MVDSF5.pick())
            self.memorize_session_then_state(NodeEdafStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeDFivehundredandeightyNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDbdaStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if Handler(self).can_handle():
            self.say(BUILTIN_TEXT_MVDSF5.pick())
            self.memorize_session_then_state(NodeEdafStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeDFivehundredandeightyNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeEdafStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if MeHandler(self).can_handle():
            self.say(BUILTIN_TEXT_PODCGV.pick())
            self.memorize_session_then_state(NodeFiftyFourEightStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeASixNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDFivehundredandeightyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if Yes_chefHandler(self).can_handle():
            self.say(BUILTIN_TEXT_0MCHOO.pick())
            self.memorize_session_then_state(NodeBThreehundredandseventyNineStateHandler)
            return self.to_platform_dict()
        
        elif No_chefHandler(self).can_handle():
            self.say(BUILTIN_TEXT_AMLZRX.pick())
            self.memorize_session_then_state(NodeSixNinetyStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBThreehundredandseventyNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesHandler(self).can_handle():
            self.say(BUILTIN_TEXT_GQUBNB.pick())
            self.memorize_session_then_state(NodeBSevenhundredandninetyFiveStateHandler)
            return self.to_platform_dict()
        
        elif Yes_chefHandler(self).can_handle():
            self.say(BUILTIN_TEXT_GQUBNB.pick())
            self.memorize_session_then_state(NodeBSevenhundredandninetyFiveStateHandler)
            return self.to_platform_dict()
        
        elif NoHandler(self).can_handle():
            self.say(BUILTIN_TEXT_AMLZRX.pick())
            self.memorize_session_then_state(NodeSixNinetyStateHandler)
            return self.to_platform_dict()
        
        elif No_chefHandler(self).can_handle():
            self.say(BUILTIN_TEXT_AMLZRX.pick())
            self.memorize_session_then_state(NodeSixNinetyStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeSixNinetyStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeSixNinetyStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeEdafStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeBSevenhundredandninetyFiveStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeEdafStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeDfcTwoStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesHandler(self).can_handle():
            self.say(BUILTIN_TEXT__FWW96.pick())
            self.memorize_session_then_state(NodeDebOneStateHandler)
            return self.to_platform_dict()
        
        elif NoHandler(self).can_handle():
            self.say(BUILTIN_TEXT_UT1TP5.pick())
            self.memorize_session_then_state(NodeFiftySevenFiveStateHandler)
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            self.memorize_session_then_state(NodeFSixtyNineStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeFiftyFourEightStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeASixNineStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if YesHandler(self).can_handle():
            self.say(BUILTIN_TEXT_H7OF88.pick())
            self.memorize_session_then_state(NodeAOneZeroStateHandler)
            return self.to_platform_dict()
        
        elif NoHandler(self).can_handle():
            self.say(BUILTIN_TEXT_H7OF88.pick())
            self.memorize_session_then_state(NodeAOneZeroStateHandler)
            return self.to_platform_dict()
        
        
    def fallback(self) -> dict:
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class NodeAOneZeroStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        pass
        
    def fallback(self) -> dict:
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
    skill_builder.add_request_handler(NodeLeostorystartRequestHandler)
    skill_builder.add_state_handler(NodeLeostorystartStateHandler)
    skill_builder.add_state_handler(TopicChoicesStateHandler)
    skill_builder.add_state_handler(CatchStateHandler)
    skill_builder.add_state_handler(NodeFiftySevenFiveStateHandler)
    skill_builder.add_state_handler(NodeDebOneStateHandler)
    skill_builder.add_state_handler(NodeFaFiftyOneStateHandler)
    skill_builder.add_state_handler(NodeTwoSeventyNineStateHandler)
    skill_builder.add_state_handler(NodeFSixtyNineStateHandler)
    skill_builder.add_state_handler(NodeDEightFiveStateHandler)
    skill_builder.add_state_handler(NodeDbdaStateHandler)
    skill_builder.add_state_handler(NodeEdafStateHandler)
    skill_builder.add_state_handler(NodeDFivehundredandeightyNineStateHandler)
    skill_builder.add_state_handler(NodeBThreehundredandseventyNineStateHandler)
    skill_builder.add_state_handler(NodeSixNinetyStateHandler)
    skill_builder.add_state_handler(NodeBSevenhundredandninetyFiveStateHandler)
    skill_builder.add_state_handler(NodeDfcTwoStateHandler)
    skill_builder.add_state_handler(NodeFiftyFourEightStateHandler)
    skill_builder.add_state_handler(NodeASixNineStateHandler)
    skill_builder.add_state_handler(NodeAOneZeroStateHandler)
    skill_builder.add_request_handler(YesHandler)
    skill_builder.add_request_handler(NoHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)
