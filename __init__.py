from .skill_builder.inoft_skill_builder import InoftSkill, InoftCondition, InoftHandler, \
    InoftRequestHandler, InoftStateHandler, InoftDefaultFallback, InoftHandlersGroup, canProcessIntentNames

from .platforms_handlers.simulator.simulator_core import Simulator
from .speechs.ssml_builder_core import Speech, SpeechsList

from .platforms_handlers.discord.handler_input import start_discord_listening

from inoft_vocal_framework.skill_settings.skill_settings import Settings

# todo: if the framework do not find the AWS credentials, ask with a dialog
#  if the developer want to run the app with the database disabled