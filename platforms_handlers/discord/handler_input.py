from collections import Callable
from discord import Message


def start_discord_listening(token: str, lambda_handler_function: Callable, command_prefix: str = "."):
    import click
    if click.confirm("Are you sure you want to trigger a Discord listening event ?"
                     "Never do that on a serverless app, since the app will keep running until closed."):
        DiscordHandlerInput.SHOULD_BE_USED = True
        DiscordHandlerInput.TOKEN = token
        DiscordHandlerInput.HANDLER_FUNCTION_TO_USE = lambda_handler_function

        from inoft_vocal_framework.platforms_handlers.discord import ClientWrapper
        DiscordHandlerInput.CLIENT_WRAPPER = ClientWrapper(prefix=command_prefix)
        DiscordHandlerInput.CLIENT_WRAPPER.run(token=token)


class DiscordHandlerInput:
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    SHOULD_BE_USED = False
    TOKEN = None
    HANDLER_FUNCTION_TO_USE = None
    CLIENT_WRAPPER = None

    def __init__(self, parent_handler_input: HandlerInput, request: Message):
        self.parent_handler_input = parent_handler_input
        self.request = request

    async def _say(self, text_or_ssml: str):
        data = {
            "author_name": self.request.author.name,
            "author_id": self.request.author.id,
            "message": text_or_ssml,
            "time": self.request.created_at
        }
        print(data)
        # public channel sending
        await self.request.channel.send(text_or_ssml)

    def say(self, text_or_ssml: str):
        import asyncio
        loop = asyncio.get_event_loop()
        loop.create_task(self._say(text_or_ssml=text_or_ssml))
        loop.run_until_complete()
        # todo: understand why this line crash, and why when this line is on, only the first message will be send

