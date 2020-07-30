

class ClientWrapper:
    def __init__(self, prefix: str = "."):
        from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.discord.discord_static_infos import DiscordStaticInfos
        DiscordStaticInfos.COMMAND_PREFIX = prefix

        from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.discord import backend_client
        self.client = backend_client.bot_client

    def run(self, token: str):
        self.client.run(token)

    async def connect(self, *, timeout=60.0, reconnect=True):
        """
        key_id, _ = self._get_voice_client_key()
        state = self._state

        if state._get_voice_client(key_id):
            raise ClientException('Already connected to a voice channel.')
        """

        from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.discord.voice_client import VoiceClient
        voice = VoiceClient(state=state, timeout=timeout, channel=self)
        state._add_voice_client(key_id, voice)

        try:
            await voice.connect(reconnect=reconnect)
        except asyncio.TimeoutError:
            try:
                await voice.disconnect(force=True)
            except Exception:
                # we don't care if disconnect failed because connection failed
                pass
            raise # re-raise

        return voice


if __name__ == "__main__":
    from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.discord.static_token import token
    client_wrapper = ClientWrapper(prefix="_")
    client_wrapper.run(token=token)

