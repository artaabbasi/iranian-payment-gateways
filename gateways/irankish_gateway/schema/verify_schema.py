from typing import Optional
from lib.gateway.schema.base_verify_schema import BaseVerifySchema


class VerifySchema(BaseVerifySchema):
    transaction_id: str
    amount: int
    res_code: str
    reference_id: str
    tracking_code: str
    token: str
