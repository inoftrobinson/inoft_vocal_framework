from inoft_vocal_framework import InoftRequestHandler, AudioBlock, InoftSkill, Settings, InoftDefaultFallback
from inoft_vocal_framework.user_data_plugins.inoft_vocal_engine_structnosql_plugin.database_clients import \
    InoftVocalEngineCachingTable
from inoft_vocal_framework.user_data_plugins.inoft_vocal_engine_structnosql_plugin.plugin import \
    UserDataInoftVocalEngineStructNoSQLPlugin
from inoft_vocal_framework.user_data_plugins.inoft_vocal_engine_structnosql_plugin.table_models import \
    BaseUserTableDataModel


class StartRequestHandler(InoftRequestHandler):
    def can_handle(self) -> bool:
        return self.is_launch_request()

    def handle(self):
        audio_block = AudioBlock()
        track1 = audio_block.create_track(primary=True)
        track1_speech1 = track1.create_speech(
            text="Alors cher ami, dis moi tout sur ce que tu vas manger ce soir !", voice_key="Lea", player_start_time=track1.player_start_time
        )
        track2 = audio_block.create_track(primary=True)
        track2_sound1 = track2.create_sound(
            file_url="https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/сплинпрочьизмоейголовы.mp3",
            player_start_time=track2.player_start_time,
            player_end_time=track2.player_start_time + 15,
        )
        """track3 = audio_block.create_track(primary=True)
        track3_sound1 = track3.create_sound(
            file_url="https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/DaftPunkSomethingAboutUsRandyGeorgeTheremin.mp3",
            player_start_time=track3.player_start
        )
        track4 = audio_block.create_track(primary=True)
        track4_sound1 = track4.create_sound(
            file_url="https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/MickGordon08FleshMetal.mp3",
            player_start_time=track4.player_start
        )
        track5 = audio_block.create_track(primary=True)
        track5_sound1 = track5.create_sound(
            file_url="https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/b1fe5939-032b-462d-92e0-a942cd445096/22ac1d08-292d-4f2e-a9e3-20d181f1f58f/files/synthchopinfantaisieimpromptu120bpm1.mp3",
            player_start_time=track5.player_start + 127.575
        )"""
        self.play_audio_block(audio_block)
        return self.to_platform_dict()


class DefaultFallback(InoftDefaultFallback):
    def handle(self):
        self.say("I did not catch that.")
        return self.to_platform_dict()


def lambda_handler(event, context):
    user_data_inoft_vocal_engine_table_client = InoftVocalEngineCachingTable(
        engine_account_id="b1fe5939-032b-462d-92e0-a942cd445096",
        engine_project_id="4ede8b70-46f6-4ae2-b09c-05a549194c8e",
        engine_api_key="a2bf5ff8-bbd3-4d01-b695-04138ee19b42",
        region_name='eu-west-3', table_id='sampleUserDataTableId',
        data_model=BaseUserTableDataModel
    )
    skill_builder = InoftSkill(Settings(
        infrastructure_speech_synthesis=Settings.INFRASTRUCTURE_LOCAL_ENGINE,
        engine_account_id="b1fe5939-032b-462d-92e0-a942cd445096",
        engine_project_id="4ede8b70-46f6-4ae2-b09c-05a549194c8e",
        engine_api_key="a2bf5ff8-bbd3-4d01-b695-04138ee19b42",
        user_data_plugin=UserDataInoftVocalEngineStructNoSQLPlugin(
            table_client=user_data_inoft_vocal_engine_table_client
        )))
    skill_builder.add_request_handler(StartRequestHandler)
    skill_builder.set_default_fallback_handler(DefaultFallback)
    return skill_builder.handle_any_platform(event=event, context=context)

if __name__ == "__main__":
    from inoft_vocal_framework import Simulator
    event_, context_ = Simulator(platform=Simulator.PLATFORM_ALEXA, event_type="launch").get_event_and_context()
    print(f"\n\nFinal Output : {lambda_handler(event=event_, context=context_)}")
