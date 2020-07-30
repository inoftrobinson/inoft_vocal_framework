from inoft_vocal_engine.inoft_vocal_framework.speechs.ssml_builder_core import SpeechsList, Speech

MSGS_WELCOME = SpeechsList(id="welcome", speechs=[
    Speech().add_text("Hello world friend !").set_prob(1),
    Speech().add_text("Hello world dude !").set_prob(1),
    Speech().add_text("Hello world love !").set_prob(0.1),
])
