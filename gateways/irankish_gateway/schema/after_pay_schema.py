from typing import Optional
from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema


class AfterPaySchema(BaseAfterPaySchema):
    systemTraceAuditNumber: Optional[str] = None
    responseCode: Optional[str] = None
    requestId: Optional[str] = None
    merchantID: Optional[str] = None
    retrievalReferenceNumber: Optional[str] = None
    maskedPan: Optional[str] = None
    token: Optional[str] = None