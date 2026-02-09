from typing import Optional
from lib.gateway.schema.base_pay_schema import BasePaySchema


class PaySchema(BasePaySchema):
    amount: int
    payment_id: Optional[int] = 0
    transaction_id: str
    description: Optional[str] = None
    mobile_number: str
    call_back_url: str

