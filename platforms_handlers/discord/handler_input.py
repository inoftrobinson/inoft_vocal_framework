from collections import Callable

import click

from inoft_vocal_framework.platforms_handlers.current_used_platform_info import CurrentUsedPlatformInfo


def start_discord_listening(server_id: str, lambda_handler_function: Callable):
    if click.confirm("Are you sure you want to trigger a Discord listening event ?"
                     "Never do that on a serverless app, since the app will keep running until closed."):
        DiscordHandlerInput.SHOULD_BE_USED = True

class DiscordHandlerInput:
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    SHOULD_BE_USED = False

    def __init__(self, parent_handler_input: HandlerInput):
        self.parent_handler_input = parent_handler_input

