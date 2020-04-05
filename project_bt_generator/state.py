from inoft_vocal_framework import InoftSkill, InoftStateHandler, InoftDefaultFallback
import os


class EntryStateHandler(InoftStateHandler):
    def handle(self):
        if YesHandler(self).can_handle():
            return self.to_platform_dict()
        
        elif NoHandler(self).can_handle():
            return self.to_platform_dict()
        
        
    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class ChoicesStateHandler(InoftStateHandler):
    def handle(self):
        if GenericHandler(self).can_handle():
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            return self.to_platform_dict()
        
        elif GenericHandler(self).can_handle():
            return self.to_platform_dict()
        
        
    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class CatchStateHandler(InoftStateHandler):
    def handle(self):
        
    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class SevenStateHandler(InoftStateHandler):
    def handle(self):
        if YesHandler(self).can_handle():
            return self.to_platform_dict()
        
        elif NoHandler(self).can_handle():
            return self.to_platform_dict()
        
        
    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class DebStateHandler(InoftStateHandler):
    def handle(self):
        if YesHandler(self).can_handle():
            return self.to_platform_dict()
        
        elif NoHandler(self).can_handle():
            return self.to_platform_dict()
        
        
    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class FaStateHandler(InoftStateHandler):
    def handle(self):
        
    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

class TwoStateHandler(InoftStateHandler):
    def handle(self):
        if GenericHandler(self).can_handle():
            return self.to_platform_dict()
        
        
    def fallback(self):
        self.say("You can say Yes or No and that's it")
        return self.to_platform_dict()

def lambda_handler(event, context):
    skill_builder = InoftSkill(settings_yaml_filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.yaml"))
    skill_builder.add_state_handler(EntryStateHandler)
    skill_builder.add_state_handler(ChoicesStateHandler)
    skill_builder.add_state_handler(CatchStateHandler)
    skill_builder.add_state_handler(SevenStateHandler)
    skill_builder.add_state_handler(DebStateHandler)
    skill_builder.add_state_handler(FaStateHandler)
    skill_builder.add_state_handler(TwoStateHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)