from typing import Optional
from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema


class AfterPaySchema(BaseAfterPaySchema):
    resCode: Optional[str]
    SaleReferenceId: Optional[str]
    SaleOrderId: Optional[str]
    CardHolderPan: Optional[str]
    RefId: Optional[str]
