from lib.gateway.datamodel.base_info_datamodel import BaseInfoDataModel


class BehpardakhtInfoDataModel(BaseInfoDataModel):
    username: str
    password: str
    terminal_id: int
