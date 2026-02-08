from gateways.sample_gateway.datamodel.gateway_transaction_datamodel import GatewayTransactionDataModel
from lib.gateway.base_transaction_repository import BaseTransactionRepository

transactions = {}

class TransactionRepository(BaseTransactionRepository):
    def __init__(self):
        super().__init__(GatewayTransactionDataModel)

    def get(self, unique_index: str) -> GatewayTransactionDataModel:
        transaction = transactions.get(unique_index, )
        if transaction is None:
            transaction = {}
        return GatewayTransactionDataModel(
            transaction_id=transaction.get('transaction_id'),
            transaction_date=transaction.get('transaction_date'),
            amount=transaction.get('amount'),
            tracking_code=transaction.get('tracking_code'),
        )

    def create(self, data: GatewayTransactionDataModel) -> GatewayTransactionDataModel:
        transaction_id = data.get('transaction_id')
        transaction = GatewayTransactionDataModel(
            transaction_id=transaction_id,
            transaction_date=data.get('transaction_date'),
            amount=data.get('amount'),
            tracking_code=data.get('tracking_code'),
        )
        transactions.update({transaction_id: transaction})
        return transaction

    def update(self, data: GatewayTransactionDataModel) -> GatewayTransactionDataModel:
        transaction_id = data.get('transaction_id')
        transaction = GatewayTransactionDataModel(
            transaction_id=transaction_id,
            transaction_date=data.get('transaction_date'),
            amount=data.get('amount'),
            tracking_code=data.get('tracking_code'),
        )
        transactions.update({transaction_id: transaction})
        return transaction

    def delete(self, unique_index: str) -> None:
        transactions.update({unique_index: None})
