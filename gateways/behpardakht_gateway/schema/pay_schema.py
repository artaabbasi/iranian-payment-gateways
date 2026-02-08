from lib.gateway.schema.base_pay_schema import BasePaySchema


class PaySchema(BasePaySchema):
    amount: int
    payment_id: str
    transaction_id: str
    description: str
    mobile_number: str
    call_back_url: str

