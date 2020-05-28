from inoft_vocal_framework import Sound

text = """
*Léo* Ont pourrais essayer de récuperer des informations en utilisant leurs radio.
*Willie* Comment ont ferrais, il faudrais qu'ils croient qu'ont soit dans leurs camp ?
*Léo* Je sais pas exactement, ont trouveras. Ont pourrais essayer de capturer un Bosch.
*Willie* Ca pourrais marcher...
"""

if __name__ == "__main__":
    from inoft_vocal_framework.audacity.client import AudacityClient
    from inoft_vocal_framework.speech_synthesis.polly.client import PollyClient
    from inoft_vocal_framework.speech_synthesis.polly import VOICES
    audacity = AudacityClient()
    """polly = PollyClient()

    leo = Sound(polly.synthesize(text="Ont pourrais essayer de récuperer des informations en utilisant leurs radio.",
                           voice_id=VOICES.French_France_Male_MATHIEU.id,
                                 filepath_to_save_to="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/speech_synthesis/polly/leo.mp3"))

    willie = Sound(polly.synthesize(text="Comment ont ferrais, il faudrais qu'ils croient qu'ont soit dans leurs camp ?",
                                    voice_id=VOICES.French_France_Female_CELINE.id,
                                    filepath_to_save_to="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/speech_synthesis/polly/willie.mp3"))
    """

    leo = Sound("F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/speech_synthesis/polly/leo.mp3")
    willie = Sound("F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/speech_synthesis/polly/willie.mp3")

    audacity.delete_all_tracks()
    audacity.import_file(leo.local_filepath, track_number=1)
    # audacity.import_file(willie.local_filepath, track_number=2)
    audacity.set_clip(clip_id=1, track_number=0, seconds_start=leo.duration_seconds)
