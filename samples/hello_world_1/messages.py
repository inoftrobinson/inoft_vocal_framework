from inoft_vocal_framework.speechs.ssml_builder_core import SpeechCategory, Speech

INTERACTION_TYPE_WELCOME = "welcome"
MSGS_FIRST_WELCOME = SpeechCategory().types(INTERACTION_TYPE_WELCOME).speechs([
    Speech().add_text("Hello world friend !").set_prob(1),
    Speech().add_text("Hello world dude !").set_prob(1),
    Speech().add_text("Hello workd love !").set_prob(0.1),
])
