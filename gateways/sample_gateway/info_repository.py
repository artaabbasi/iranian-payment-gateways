from gateways.sample_gateway.datamodel.gateway_info_datamodel import GatewayInfoDataModel
from lib.gateway.base_info_repository import BaseInfoRepository

infos = {}

class InfoRepository(BaseInfoRepository):
    def __init__(self):
        super().__init__(GatewayInfoDataModel)

    def get(self, unique_index: str) -> GatewayInfoDataModel:
        info = infos.get(unique_index, {})
        return GatewayInfoDataModel(
            username=info.get('username'),
            password=info.get('password'),
        )

    def create(self, data: GatewayInfoDataModel) -> GatewayInfoDataModel:
        username = data.get('username')
        info = GatewayInfoDataModel(
            username=username,
            password=data.get('password'),
        )
        infos.update({username: info})
        return info

    def update(self, data: GatewayInfoDataModel) -> GatewayInfoDataModel:
        username = data.get('username')
        info = GatewayInfoDataModel(
            username=username,
            password=data.get('password'),
        )
        infos.update({username: info})
        return info

    def delete(self, unique_index: str) -> None:
        infos.update({unique_index: None})
