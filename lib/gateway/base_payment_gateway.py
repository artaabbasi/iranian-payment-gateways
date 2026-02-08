from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any
from lib.gateway.datamodel.base_info_datamodel import BaseInfoDataModel
from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema
from lib.gateway.schema.base_pay_schema import BasePaySchema
from lib.gateway.schema.base_verify_schema import BaseVerifySchema
from lib.gateway.schema.pay_out_schema import PayOutSchema
from lib.gateway.schema.verify_out_schema import VerifyOutSchema

P = TypeVar('P', bound=BasePaySchema)
AP = TypeVar('AP', bound=BaseAfterPaySchema)
V = TypeVar('V', bound=BaseVerifySchema)
I = TypeVar('I', bound=BaseInfoDataModel)

class BasePaymentGateway(ABC, Generic[P, AP, V, I]):
    def __init__(self, info: I):
        self._info = info

    @abstractmethod
    def pay(self, data: P) -> PayOutSchema:
        raise Exception("Defining `pay` is required.")

    @abstractmethod
    def verify(self, data: V) -> VerifyOutSchema:
        raise Exception("Defining `verify` is required.")

    @abstractmethod
    def after_pay(self, data: AP) -> Any:
        raise Exception("Defining `after_pay` is required.")

    async def a_pay(self, data: P) -> PayOutSchema:
        return self.pay(data)

    async def a_verify(self, data: V) -> VerifyOutSchema:
        return self.verify(data)

    async def a_after_pay(self, data: AP) -> Any:
        return self.after_pay(data)
