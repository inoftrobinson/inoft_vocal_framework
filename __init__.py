from .skill_builder.inoft_skill_builder import InoftSkill, InoftCondition, InoftHandler, \
    InoftRequestHandler, InoftStateHandler, InoftDefaultFallback, InoftHandlersGroup, canProcessIntentNames

from .platforms_handlers.simulator.simulator_core import Simulator
from .speechs.ssml_builder_core import Speech, SpeechsList

# from .platforms_handlers.discord.handler_input import start_discord_listening
# todo: re-implement discord integration without requiring its dependencies to use other platforms

from inoft_vocal_framework.skill_settings.skill_settings import Settings
from inoft_vocal_framework.audio_engine import audio_engine_wrapper
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock
from inoft_vocal_framework.audio_editing import audio_effects

from inoft_vocal_framework.user_data_plugins.base_plugin import UserDataBasePlugin
from inoft_vocal_framework.user_data_plugins import inoft_vocal_engine_structnosql_plugin

# todo: if the framework do not find the AWS credentials, ask with a dialog
#  if the developer want to run the app with the database disabled
