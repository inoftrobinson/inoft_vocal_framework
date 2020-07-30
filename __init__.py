from inoft_vocal_engine.inoft_vocal_framework.skill_builder.inoft_skill_builder import InoftSkill, InoftCondition, InoftHandler,\
    InoftRequestHandler, InoftStateHandler, InoftDefaultFallback, InoftHandlersGroup

from inoft_vocal_engine.inoft_vocal_framework.speechs.ssml_builder_core import Speech, SpeechsList
from .audio_editing.audioclip import AudioClip, Sound, Track, Relation

from inoft_vocal_engine.inoft_vocal_framework.skill_settings.skill_settings import Settings


# todo: if the framework do not find the AWS credentials, ask with a dialog
#  if the developer want to run the app with the database disabled
