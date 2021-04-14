from pydantic import Field
from pydantic.main import BaseModel
from typing import Optional, Union


class Context(BaseModel):
    json_key = "context"

    class SystemModel(BaseModel):
        apiEndpoint: Optional[str] = None
        apiAccessToken: Optional[str] = None

        class ApplicationModel(BaseModel):
            json_key = "application"
            applicationId: Optional[str] = None
        application: ApplicationModel

        class UserModel(BaseModel):
            json_key = "user"
            userId: Optional[str] = None
        user: UserModel

        class DeviceModel(BaseModel):
            json_key = "device"

            deviceId: Optional[str] = None
            class SupportedInterfacesModel(BaseModel):
                json_key = "supportedInterfaces"
                # todo: complete the supported interfaces class
            supportedInterfaces: SupportedInterfacesModel
        device: DeviceModel
    system: SystemModel = Field(alias='System')

    class AudioPlayerModel(BaseModel):
        json_key = "AudioPlayer"
        PLAYER_ACTIVITY_STOPPED = "STOPPED"

        offsetInMilliseconds: Optional[int] = None
        token: Optional[str] = None
        playerActivity: Optional[Union[PLAYER_ACTIVITY_STOPPED]] = None
    audioPlayer: Optional[AudioPlayerModel] = Field(alias='AudioPlayer')
