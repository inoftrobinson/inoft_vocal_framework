import os
from inoft_vocal_engine import InoftSkill, InoftRequestHandler, InoftStateHandler, InoftDefaultFallback


class StartRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self) -> dict:
        if not self.google.has_user_granted_push_notifications_permission():
            self.say("Ca vous dirait que je vous envoie une notification quand le prochain chapitre sort ?")
            self.memorize_session_then_state(OfferNotificationsSubscriptionStateHandler)
        else:
            self.say("Vous êtes déjà abonner aux notifications pour le prochain chapitre ! Aller salut.")
            self.end_session()

        return self.to_platform_dict()


class OfferNotificationsSubscriptionStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.is_in_intent_names("Yes"):
            self.say("Très bien ! Google Assistant vas vous demander l'autorisation de vous envoyer les notifications.")
            self.google.request_push_notifications_permission_if_missing(intent_name="actions.intent.MAIN")
            self.memorize_session_then_state(NotificationsSubscriptionsCallbacksStateHandler)

        elif self.is_in_intent_names("No"):
            self.say("Vous êtes vraiment méchant ! Je boude maintenant, aurevoir.")
            self.end_session()

        return self.to_platform_dict()

    def fallback(self) -> dict:
        self.say("Alors, vous voulez que je vous inscrive aux notifications ? Oui, non ?")
        return self.to_platform_dict()


class NotificationsSubscriptionsCallbacksStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.google.has_user_granted_push_notifications_permission():
            self.google.subscribe_current_user_to_notifications_group("nextChapterRelease")
            self.say("Super, je vous ai abonné ! Excellente journée à vous !")
            self.end_session()
        else:
            self.say("C'est vraiment pas sympa de ne pas avoir accepté les notifications ! Je vous fais la tête, aller salut.")
            self.end_session()

        return self.to_platform_dict()


class DefaultFallback(InoftDefaultFallback):
    def handle(self):
        self.say("J'ai aucune idée de ce que vous voulez dire. Aller salut.")
        self.end_session()
        return self.to_platform_dict()


def lambda_handler(event, context):
    skill = InoftSkill()
    skill.add_request_handler(StartRequestHandler)
    skill.add_state_handler(OfferNotificationsSubscriptionStateHandler)
    skill.add_state_handler(NotificationsSubscriptionsCallbacksStateHandler)
    skill.set_default_fallback_handler(DefaultFallback)
    return skill.handle_any_platform(event=event, context=context)

if __name__ == "__main__":
    from inoft_vocal_engine import Simulator
    event_, context_ = Simulator(platform=Simulator.PLATFORM_GOOGLE, event_type="launch").get_event_and_context()
    # event_, context_ = Simulator(platform=Simulator.PLATFORM_GOOGLE, event_type="grant_update_permissions").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event_, context=context_)}")
