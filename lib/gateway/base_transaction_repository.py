from abc import ABC
from typing import TypeVar, Type

from lib.gateway.base_repository import BaseRepository
from lib.gateway.datamodel.base_gateway_transaction_datamodel import BaseGatewayTransactionDataModel

T = TypeVar('T', bound=BaseGatewayTransactionDataModel)

class BaseTransactionRepository(BaseRepository, ABC):
    def __init__(self, entity_type: Type[T]):
        super().__init__(entity_type)