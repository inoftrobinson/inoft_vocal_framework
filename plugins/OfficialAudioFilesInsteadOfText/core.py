import os
from inoft_vocal_engine.plugins.plugin_base import PluginCodeGenerationBase


class Core(PluginCodeGenerationBase):
    from inoft_vocal_engine.botpress_integration.generator import GeneratorCore

    def execute(self, generator_core: GeneratorCore):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        generator_core.templates.say_action_template = os.path.join(current_dir, "say_action.tem")

        bucket_name = "test-vocal-export-inoft"
        bucket_region = "eu-west-3"

        for say_action in generator_core.say_actions:
            say_action.code = f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{say_action.message_id_to_say}/compressed_final_render.mp3"
