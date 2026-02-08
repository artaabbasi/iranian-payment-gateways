import datetime
from typing import Optional
from pydantic import BaseModel


class GatewayTransactionDataModel(BaseModel):
    transaction_id: str
    transaction_date: Optional[datetime.datetime] = None
    amount: int
    tracking_code: Optional[int] = None
