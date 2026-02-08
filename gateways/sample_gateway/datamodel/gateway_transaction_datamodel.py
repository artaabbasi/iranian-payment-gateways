import datetime
from typing import Optional

from lib.gateway.datamodel.base_gateway_transaction_datamodel import BaseGatewayTransactionDataModel


class GatewayTransactionDataModel(BaseGatewayTransactionDataModel):
    transaction_id: str
    transaction_date: Optional[datetime.datetime] = None
    amount: int
    tracking_code: Optional[int] = None
