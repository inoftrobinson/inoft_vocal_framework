from pydantic import Field
from pydantic.main import BaseModel
from typing import Optional


class Context(BaseModel):
    class SystemModel(BaseModel):
        apiEndpoint: Optional[str] = None
        apiAccessToken: Optional[str] = None

        class ApplicationModel(BaseModel):
            applicationId: Optional[str] = None
        application: ApplicationModel

        class UserModel(BaseModel):
            userId: Optional[str] = None
        user: UserModel

        class DeviceModel(BaseModel):
            deviceId: Optional[str] = None
            class SupportedInterfacesModel(BaseModel):
                pass
                # todo: complete the supported interfaces class
            supportedInterfaces: SupportedInterfacesModel
        device: DeviceModel
    system: SystemModel = Field(alias='System')

    class AudioPlayerModel(BaseModel):
        PLAYER_ACTIVITY_STOPPED = "STOPPED"

        offsetInMilliseconds: Optional[int] = None
        token: Optional[str] = None
        playerActivity: Optional[str] = None
    audioPlayer: Optional[AudioPlayerModel] = Field(alias='AudioPlayer', default=None)
