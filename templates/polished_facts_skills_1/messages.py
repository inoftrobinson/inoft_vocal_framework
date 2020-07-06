from inoft_vocal_engine import SpeechsList, Speech

MSGS_START_FACT = SpeechsList(id="startFactPhrase", speechs=[
    Speech().add_text("Did you know").set_prob(1),
    Speech().add_text("Have you heard").set_prob(1),
    Speech().add_text("Did you suspected").set_prob(0.5)
])

MSGS_END_FACT = SpeechsList(id="endFactPhrase", speechs=[
    Speech().add_text("Don't you found it wild ?").set_prob(0.5),
    Speech().add_text("Don't you found it crazy ?").set_prob(1),
    Speech().add_text("Crazy, right ?").set_prob(1),
    Speech().add_text("Its not crazy to you ? It is for me !").set_prob(1),
])

MSGS_NEW_FACT = SpeechsList(id="newFactCallToAction", speechs=[
    Speech().add_text("Ready for a new fact ?").set_prob(1),
    Speech().add_text("Do you want another fact ?").set_prob(1),
])

MSGS_FACTS = SpeechsList(id="mainFacts", speechs=[
    Speech().add_text("that the Inoft Vocal Framework was the first package from Robinson Labourdette ? He did not even knew how to publish it !").set_prob(1),
    Speech().add_text("that for simpler use of the framework and the processing of the requests, a new object type, the SafeDict, has been created ?").set_prob(1),
    Speech().add_text("that i'm starting to be out of inspiration ?").set_prob(0.1)
])
