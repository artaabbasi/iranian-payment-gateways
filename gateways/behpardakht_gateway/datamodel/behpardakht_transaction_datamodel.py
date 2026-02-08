import datetime
from typing import Optional
from pydantic import BaseModel


class GatewayTransactionDataModel(BaseModel):
    res_code: Optional[str] = None
    sale_reference_id: Optional[str] = None
    order_id: Optional[str] = None
    card_number: Optional[str] = None
    ref_id: Optional[str] = None