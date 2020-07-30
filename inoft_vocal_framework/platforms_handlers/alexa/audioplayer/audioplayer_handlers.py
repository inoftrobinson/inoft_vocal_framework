import logging

from inoft_vocal_engine.inoft_vocal_framework.skill_builder.inoft_skill_builder import InoftHandlersGroup


class AlexaAudioPlayerHandlers(InoftHandlersGroup):
    from inoft_vocal_engine.inoft_vocal_framework.skill_builder.inoft_skill_builder import InoftRequestHandler

    def __init__(self, parent_handler, additional_pause_intents_names: list = None,
                 additional_resume_intent_names: list = None):

        self.onPauseHandler = self.OnPauseHandler(parent_handler=parent_handler, intents_names=additional_pause_intents_names)
        self.onResumeHandler = self.OnResumeHandler(parent_handler=parent_handler, intent_names=additional_resume_intent_names)

    class OnPauseHandler(InoftRequestHandler):
        def __init__(self, parent_handler, intents_names: list):
            super().__init__(parent_handler=parent_handler)
            default_intents_names = ["AMAZON.PauseIntent"]
            self.intents_names = default_intents_names + intents_names if isinstance(intents_names, list) else default_intents_names
            self.request_types = ["PlaybackController.PauseCommandIssued"]

        def can_handle(self) -> bool:
            if self.is_in_intent_names(self.intents_names) or self.alexa.is_in_request_types(self.request_types):
                return True

        def handle(self) -> dict:
            self.say("Pause Request Received ! Please customize this message.")

            last_played_item = self.alexa.audioplayer.get_last_played_item()
            if last_played_item is not None:
                offset_in_milliseconds = self.alexa.audioplayer.offset_in_milliseconds
                if isinstance(offset_in_milliseconds, (int, float)) and offset_in_milliseconds > 0:
                    last_played_item.offset_in_milliseconds = offset_in_milliseconds
                    self.alexa.audioplayer.memorize_audio_item(last_played_item)
                    # We change the offset in milliseconds of the last played item, then we
                    # memorize the item back, in order to save its new modified offset value.

            self.alexa.audioplayer.stop()
            return self.to_platform_dict()

    class OnResumeHandler(InoftRequestHandler):
        def __init__(self, parent_handler, intent_names: list):
            super().__init__(parent_handler=parent_handler)
            default_intent_names = ["AMAZON.ResumeIntent"]
            self.intent_names = default_intent_names + intent_names if isinstance(intent_names, list) else default_intent_names
            self.request_types = ["PlaybackController.PlayCommandIssued"]

        def can_handle(self) -> bool:
            if self.is_in_intent_names(self.intent_names) or self.alexa.is_in_request_types(self.request_types):
                return True

        def handle(self) -> dict:
            if (self.alexa.audioplayer.token is not None
            and self.alexa.audioplayer.player_activity == self.alexa.audioplayer.PLAYER_ACTIVITY_STOPPED):
                last_played_item = self.alexa.audioplayer.get_last_played_item()
                if last_played_item is not None:
                    # Normally when resuming an audio media with the audioplayer, we should have an id for the last played
                    # item, and found it in the items dict. Yet it is possible for the id or the item to not be present if
                    # there has been some kind of manual or automatic reset of the user data in the database, and not in the
                    # alexa memory that remember that he had interacted with an audio player.
                    self.alexa.audioplayer.play_item(audio_item=last_played_item)
                    logging.debug(f"Resuming audio file with id {last_played_item.identifier} and title {last_played_item.title}")
                    return self.to_platform_dict()
                else:
                    # You should respond something like this :
                    self.say("Unfortunately i have not been able to find the track/podcast you last played. " +
                             "It's strange, it never happens to me. In the mean time that i found what happened, " +
                             "i can play a track/podcast that i think you would like. Are you up to it ?")
                    # And then have your custom logic to make it happen.

                    raise Exception("NOT IMPLEMENTED - What happens if the user is trying to ask the AudioPlayer to resume, that the"
                                    "AudioPlayer object is found in the request, yet that the last item played by the user has not"
                                    "been found in its playing history. This can happen if you have cleared the users data.")
            else:
                last_played_item = self.alexa.audioplayer.get_last_played_item()
                # todo: finish

                raise Exception("NOT IMPLEMENTED - What happens if the user is trying to ask the AudioPlayer to resume, that the"
                                "AudioPlayer object is found in the request, yet that the last item played by the user has not"
                                "been found in its playing history. This can happen if you have cleared the users data.")


    class OnPossibleResumeHandler(InoftRequestHandler):
        def __init__(self, parent_handler, intent_names: list):
            super().__init__(parent_handler=parent_handler)
            self.intent_names = intent_names if isinstance(intent_names, list) else list()

        def can_handle(self) -> bool:
            if (self.alexa.audioplayer.token is not None
            and self.alexa.audioplayer.player_activity == self.alexa.audioplayer.PLAYER_ACTIVITY_STOPPED):
                return True

        def handle(self):
            if (self.alexa.audioplayer.token is not None
            and self.alexa.audioplayer.player_activity == self.alexa.audioplayer.PLAYER_ACTIVITY_STOPPED):
                pass

    class OnNextHandler(InoftRequestHandler):
        def __init__(self, parent_handler, intent_names: list):
            super().__init__(parent_handler=parent_handler)
            default_intent_names = ["AMAZON.NextIntent"]
            self.intent_names = default_intent_names + intent_names if isinstance(intent_names, list) else default_intent_names
            self.request_types = ["PlaybackController.NextCommandIssued"]

        def can_handle(self) -> bool:
            if self.is_in_intent_names(self.intent_names) or self.alexa.is_in_request_types(self.request_types):
                return True

        def handle(self):
            raise Exception(f"Not implemented. You must customize this handler.")

    class OnPreviousHandler(InoftRequestHandler):
        def __init__(self, parent_handler, intent_names: list):
            super().__init__(parent_handler=parent_handler)
            default_intent_names = ["AMAZON.PreviousIntent"]
            self.intent_names = default_intent_names + intent_names if isinstance(intent_names, list) else default_intent_names
            self.request_types = ["PlaybackController.PreviousCommandIssued"]

        def can_handle(self) -> bool:
            if self.is_in_intent_names(self.intent_names) or self.alexa.is_in_request_types(self.request_types):
                return True

        def handle(self):
            raise Exception(f"Not implemented. You must customize this handler.")



