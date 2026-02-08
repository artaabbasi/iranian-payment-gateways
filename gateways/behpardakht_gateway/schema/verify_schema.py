from lib.gateway.schema.base_verify_schema import BaseVerifySchema


class VerifySchema(BaseVerifySchema):
    transaction_id: str
    amount: int
    sale_reference_id: str
