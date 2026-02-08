from abc import ABC
from typing import TypeVar, Type

from lib.gateway.base_repository import BaseRepository
from lib.gateway.datamodel.base_gateway_info_datamodel import BaseGatewayInfoDataModel

T = TypeVar('T', bound=BaseGatewayInfoDataModel)

class BaseInfoRepository(BaseRepository, ABC):
    def __init__(self, entity_type: Type[T]):
        super().__init__(entity_type)
