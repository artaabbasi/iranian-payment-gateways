from lib.gateway.schema import BaseVerifySchema


class VerifySchema(BaseVerifySchema):
    transaction_id: str
    amount: int
