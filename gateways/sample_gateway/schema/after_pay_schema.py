from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema


class AfterPaySchema(BaseAfterPaySchema):
    transaction_id: str
    amount: int
    tracking_code: int
