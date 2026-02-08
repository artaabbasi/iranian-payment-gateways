from typing import TypeVar, Dict, Type

from gateways.sample_gateway.sample_gateway import SampleGateway
from lib.gateway.base_payment_gateway import BasePaymentGateway

G = TypeVar('G', bound=BasePaymentGateway)

gateway_map: Dict[str, Type[BasePaymentGateway]] = {
    "sample": SampleGateway,
}

def get_gateway_from_name(name: str) -> Type[BasePaymentGateway]:
    return gateway_map[name]
