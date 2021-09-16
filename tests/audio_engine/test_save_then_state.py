from inoft_vocal_framework import InoftRequestHandler, AudioBlock, InoftSkill, Settings, InoftDefaultFallback, \
    InoftStateHandler
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
            text="Dis moi oui ou non !", voice_key="Lea", player_start_time=track1.player_start_time
        )
        self.play_audio_block(audio_block)
        self.memorize_session_then_state(EntryStateHandler)
        return self.to_platform_dict()

class EntryStateHandler(InoftStateHandler):
    def handle(self) -> dict:
        if self.is_in_intent_names(intent_names_list=['Yes']):
            audio_block = AudioBlock()
            track1 = audio_block.create_track()
            track1_speech1 = track1.create_speech(
                text="Il à dis oui !", voice_key="Lea",
                player_start_time=track1.player_start_time
            )
            self.play_audio_block(audio_block)
            # self.alexa.audioplayer.play("https://test-vocal-export-inoft.s3.eu-west-3.amazonaws.com/builtin_text-S08PBO/compressed_final_render.mp3")
            # self.google.play_audio("https://test-vocal-export-inoft.s3.eu-west-3.amazonaws.com/builtin_text-S08PBO/compressed_final_render.mp3")
            return self.to_platform_dict()
        elif self.is_in_intent_names(intent_names_list=['No']):
            audio_block = AudioBlock()
            track1 = audio_block.create_track()
            track1_speech1 = track1.create_speech(
                text="Il à dis non le méchant !", voice_key="Lea",
                player_start_time=track1.player_start_time
            )
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
