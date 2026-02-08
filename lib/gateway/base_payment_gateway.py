from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema
from lib.gateway.schema.base_pay_schema import BasePaySchema
from lib.gateway.schema.base_verify_schema import BaseVerifySchema
from lib.gateway.schema.pay_out_schema import PayOutSchema
from lib.gateway.schema.verify_out_schema import VerifyOutSchema

P = TypeVar('P', bound=BasePaySchema)
AP = TypeVar('AP', bound=BaseAfterPaySchema)
V = TypeVar('V', bound=BaseVerifySchema)

class BasePaymentGateway(ABC, Generic[P, AP, V]):

    @abstractmethod
    def pay(self, data: P) -> PayOutSchema:
        raise Exception("Defining `pay` is required.")

    @abstractmethod
    def verify(self, data: V) -> VerifyOutSchema:
        raise Exception("Defining `verify` is required.")

    @abstractmethod
    def after_pay(self, data: AP) -> None:
        raise Exception("Defining `after_pay` is required.")

    async def a_pay(self, data: P) -> PayOutSchema:
        return self.pay(data)

    async def a_verify(self, data: V) -> VerifyOutSchema:
        return self.verify(data)

    async def a_after_pay(self, data: AP) -> None:
        return self.after_pay(data)
