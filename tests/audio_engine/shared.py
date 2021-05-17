from inoft_vocal_framework import AudioBlock

TEST_ACCOUNT_KWARGS = {
    'override_engine_base_url': "http://127.0.0.1:5000",
    'engine_account_id': "b1fe5939-032b-462d-92e0-a942cd445096",
    'engine_project_id': "4ede8b70-46f6-4ae2-b09c-05a549194c8e",
    'engine_api_key': "a2bf5ff8-bbd3-4d01-b695-04138ee19b42",
}

__bases = {'num_channels': 1, 'sample_rate': 24000, 'bitrate': 48}
ALEXA_BASE_MANUAL_RENDER_KWARGS = {'export_target': AudioBlock.EXPORT_TARGET_LOCAL, **__bases, **TEST_ACCOUNT_KWARGS}
ALEXA_MANUAL_RENDER_CLOUD_KWARGS = {'export_target': AudioBlock.EXPORT_TARGET_MANAGED_ENGINE, **__bases, **TEST_ACCOUNT_KWARGS}
