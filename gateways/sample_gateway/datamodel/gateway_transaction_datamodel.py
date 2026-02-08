import datetime

from lib.gateway.datamodel.base_gateway_transaction_datamodel import BaseGatewayTransactionDataModel


class GatewayTransactionDataModel(BaseGatewayTransactionDataModel):
    transaction_id: str
    transaction_date: datetime.datetime
    amount: int
    tracking_code: int
