class ClientWrapper:
    def __init__(self, prefix: str = "."):
        from inoft_vocal_framework.platforms_handlers.discord.discord_static_infos import DiscordStaticInfos
        DiscordStaticInfos.COMMAND_PREFIX = prefix

        from inoft_vocal_framework.platforms_handlers.discord import backend_client
        self.client = backend_client.bot_client

    def run(self, token: str):
        self.client.run(token)


if __name__ == "__main__":
    from inoft_vocal_framework.platforms_handlers.discord.static_token import token
    ClientWrapper(prefix="_").run(token=token)
