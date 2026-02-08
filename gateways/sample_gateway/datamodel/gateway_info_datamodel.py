from pydantic import BaseModel


class GatewayInfoDataModel(BaseModel):
    username: str
    password: str
