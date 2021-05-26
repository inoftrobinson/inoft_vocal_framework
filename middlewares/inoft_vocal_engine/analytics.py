import json
from json import JSONDecodeError
from typing import Optional

import requests
from pydantic import BaseModel, ValidationError

from inoft_vocal_framework import InoftSkill, Settings
from inoft_vocal_framework.middlewares.base_middleware import BaseMiddleware


class SuccessResponseDataModel(BaseModel):
    interactionId: str
    class TracingUrlModel(BaseModel):
        presignedPostData: dict
        expectedS3FileUrl: str
    tracingUrl: TracingUrlModel


class InteractionLogger(BaseMiddleware):
    _MIDDLEWARE_KEY = 'inoft-vocal-engine_interaction-logger'

    def __init__(self, skill):
        super().__init__(skill=skill)
        self.prepared_interaction_id: Optional[str] = None
        self.prepared_tracing_presigned_post_url_data: Optional[dict] = None
        self.prepared_tracing_expected_s3_url: Optional[str] = None
        self.prepare()

    def prepare(self):
        base_project_api_url = f"http://127.0.0.1:5000/api/v1/{InoftSkill.APP_SETTINGS.engine_account_id}/{InoftSkill.APP_SETTINGS.engine_project_id}"
        response = requests.post(
            url=f"{base_project_api_url}/analytics/interactions/prepare-new",
            json={'accessToken': InoftSkill.APP_SETTINGS.engine_api_key}
        )
        try:
            response_data: dict = response.json()
            success: bool = response_data.get('success', False)
            if success is True:
                try:
                    validated_request_data = SuccessResponseDataModel(**response_data)
                    self.prepared_interaction_id = validated_request_data.interactionId
                    self.prepared_tracing_presigned_post_url_data = validated_request_data.tracingUrl.presignedPostData
                    self.prepared_tracing_expected_s3_url = validated_request_data.tracingUrl.expectedS3FileUrl
                except ValidationError as e:
                    print(e)
                    return None
        except JSONDecodeError as e:
            print(e)
            return None

    def on_interaction_end(self):
        data = {
            'interactionId': self.prepared_interaction_id,
            'userId': self.skill.handler_input.persistent_user_id,
            'platformType': self.skill.handler_input.platform,
            # 'deviceType': self.skill.handler_input.alexaHandlerInput.
            'latencyTime': self.skill.handler_input.trace.elapsed,
            'responseTime': 0,
            'tracingIsAvailable': True,
            'fields': {}
        }
        serialized_trace: dict = self.skill.handler_input.trace.serialize()

        filename: str = self.prepared_tracing_presigned_post_url_data['fields']['key'].split('/')[-1]
        trace_upload_response = requests.post(
            url=self.prepared_tracing_presigned_post_url_data.get('url', None),
            data=self.prepared_tracing_presigned_post_url_data.get('fields', {}),
            files={'file': (filename, json.dumps(serialized_trace))}
        )

        base_project_api_url = f"http://127.0.0.1:5000/api/v1/{InoftSkill.APP_SETTINGS.engine_account_id}/{InoftSkill.APP_SETTINGS.engine_project_id}"
        response = requests.post(
            url=f"{base_project_api_url}/analytics/interactions/post-prepared",
            json={**data, 'accessToken': InoftSkill.APP_SETTINGS.engine_api_key}
        )
        print(response)

if __name__ == '__main__':
    _skill = InoftSkill(Settings(
        engine_account_id="b1fe5939-032b-462d-92e0-a942cd445096",
        engine_project_id="4ede8b70-46f6-4ae2-b09c-05a549194c8e",
        engine_api_key="a2bf5ff8-bbd3-4d01-b695-04138ee19b42",
        infrastructure_speech_synthesis=Settings.INFRASTRUCTURE_NEXT_ENGINE
    ))
    InteractionLogger(skill=_skill).prepare()
