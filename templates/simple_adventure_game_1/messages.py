from inoft_vocal_engine.inoft_vocal_framework.speechs.ssml_builder_core import SpeechsList, Speech

INTERACTION_TYPE_WELCOME = "welcome"
MSGS_WELCOME = SpeechsList(id="1", speechs=[
    Speech().add_text("Bienvenue dans le jeu ! Votre but seras simple, atteindre la fin ! Prêt à jouer ?").set_prob(1),
])

MSGS_YES = SpeechsList("2", [Speech().add_text("Très bien ! ").set_prob(1)])
