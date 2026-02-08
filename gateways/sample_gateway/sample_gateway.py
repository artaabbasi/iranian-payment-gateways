from datetime import datetime
import uuid

from gateways.sample_gateway.datamodel.gateway_info_datamodel import GatewayInfoDataModel
from gateways.sample_gateway.datamodel.gateway_transaction_datamodel import GatewayTransactionDataModel
from gateways.sample_gateway.info_repository import InfoRepository
from gateways.sample_gateway.schema.after_pay_schema import AfterPaySchema
from gateways.sample_gateway.schema.pay_schema import PaySchema
from gateways.sample_gateway.schema.verify_schema import VerifySchema
from gateways.sample_gateway.transaction_repository import TransactionRepository
from lib.gateway.base_payment_gateway import BasePaymentGateway
from lib.gateway.schema.pay_out_schema import PayOutSchema
from lib.gateway.schema.verify_out_schema import VerifyOutSchema


class SampleGateway(BasePaymentGateway):
    def __init__(self):
        self._transaction_repository = TransactionRepository()
        self._transaction_type = GatewayTransactionDataModel

    def pay(self, data: PaySchema) -> PayOutSchema:
        print(f"Paying {data.amount}")
        uid = uuid.uuid4()
        self._transaction_repository.create(
            self._transaction_type(
                transaction_id=str(uid),
                amount=data.amount,
            )
        )
        return PayOutSchema(
            url=str(f"sample.ir/{uid}"),
            transaction_id=str(uid)
        )

    def verify(self, data: VerifySchema) -> VerifyOutSchema:
        print(f"Verifying {data.transaction_id}: {data.amount}")
        transaction = self._transaction_repository.get(data.transaction_id)
        return VerifyOutSchema(
            verified=bool(transaction.tracking_code),
        )

    def after_pay(self, data: AfterPaySchema) -> None:
        print(f"After paying {data.transaction_id}: {data.amount} with tracking code: {data.tracking_code}")
        self._transaction_repository.update(
            self._transaction_type(
                transaction_id=data.transaction_id,
                transaction_date=datetime.now(),
                amount=data.amount,
                tracking_code=data.tracking_code
            )
        )

