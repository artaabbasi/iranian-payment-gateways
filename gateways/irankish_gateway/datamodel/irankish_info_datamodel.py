from enum import StrEnum

from lib.gateway.datamodel.base_info_datamodel import BaseInfoDataModel


class IranKishInfoDataModel(BaseInfoDataModel):
    terminal_id: str
    acceptor_id: str
    pass_phrase: int
    rsa_public_key_file_path: str
