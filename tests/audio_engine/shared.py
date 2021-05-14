from inoft_vocal_framework import AudioBlock

__bases = {'num_channels': 1, 'sample_rate': 24000, 'bitrate': 48}
ALEXA_BASE_MANUAL_RENDER_KWARGS = {'export_target': AudioBlock.EXPORT_TARGET_LOCAL, **__bases}
ALEXA_MANUAL_RENDER_CLOUD_KWARGS = {'export_target': AudioBlock.EXPORT_TARGET_MANAGED_ENGINE, **__bases}
