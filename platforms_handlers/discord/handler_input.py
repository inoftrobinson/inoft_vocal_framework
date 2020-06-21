from collections import Callable

import click

from inoft_vocal_framework.platforms_handlers.current_used_platform_info import CurrentUsedPlatformInfo


def start_discord_listening(token: str, lambda_handler_function: Callable, command_prefix: str = "."):
    if click.confirm("Are you sure you want to trigger a Discord listening event ?"
                     "Never do that on a serverless app, since the app will keep running until closed."):
        DiscordHandlerInput.SHOULD_BE_USED = True
        DiscordHandlerInput.TOKEN = token
        DiscordHandlerInput.HANDLER_FUNCTION_TO_USE = lambda_handler_function

        from inoft_vocal_framework.platforms_handlers.discord.client_wrapper import ClientWrapper
        DiscordHandlerInput.CLIENT_WRAPPER = ClientWrapper(prefix=command_prefix)
        DiscordHandlerInput.CLIENT_WRAPPER.run(token=token)


class DiscordHandlerInput:
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    SHOULD_BE_USED = False
    TOKEN = None
    HANDLER_FUNCTION_TO_USE = None
    CLIENT_WRAPPER = None

    def __init__(self, parent_handler_input: HandlerInput):
        self.parent_handler_input = parent_handler_input

