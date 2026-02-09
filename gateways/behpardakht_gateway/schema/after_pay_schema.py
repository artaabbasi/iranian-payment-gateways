from typing import Optional
from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema


class AfterPaySchema(BaseAfterPaySchema):
    resCode: Optional[str] = None
    SaleReferenceId: Optional[str] = None
    SaleOrderId: Optional[str] = None
    CardHolderPan: Optional[str] = None
    RefId: Optional[str] = None
