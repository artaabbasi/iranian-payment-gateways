from lib.gateway.schema import BaseAfterPaySchema


class AfterPaySchema(BaseAfterPaySchema):
    transaction_id: str
    amount: int
    tracking_code: int
