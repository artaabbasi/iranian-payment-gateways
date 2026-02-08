from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema


class AfterPaySchema(BaseAfterPaySchema):
    resCode: str
    SaleReferenceId: str
    SaleOrderId: str
    CardHolderPan: str
    RefId: str