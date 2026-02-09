from typing import Optional
from lib.gateway.schema.base_after_pay_schema import BaseAfterPaySchema


class AfterPaySchema(BaseAfterPaySchema):
    systemTraceAuditNumber: Optional[str]
    responseCode: Optional[str]
    requestId: Optional[str]
    merchantID: Optional[str]
    retrievalReferenceNumber: Optional[str]
    systemTraceAuditNumber: Optional[str]
    maskedPan: Optional[str]
    token: Optional[str]