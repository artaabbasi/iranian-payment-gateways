from datetime import datetime
import uuid

from gateways.sample_gateway.datamodel.gateway_info_datamodel import GatewayInfoDataModel
from gateways.sample_gateway.schema.after_pay_schema import AfterPaySchema
from gateways.sample_gateway.schema.pay_schema import PaySchema
from gateways.sample_gateway.schema.verify_schema import VerifySchema
from lib.gateway.base_payment_gateway import BasePaymentGateway
from lib.gateway.schema.pay_out_schema import PayOutSchema
from lib.gateway.schema.verify_out_schema import VerifyOutSchema


class SampleGateway(BasePaymentGateway):
    def __init__(self , info: GatewayInfoDataModel):
        super().__init__(info)

    def pay(self, data: PaySchema) -> PayOutSchema:
        print(f"Paying {data.amount}")
        uid = uuid.uuid4()
        return PayOutSchema(
            url=str(f"sample.ir/{uid}"),
            transaction_id=str(uid)
        )

    def verify(self, data: VerifySchema) -> VerifyOutSchema:
        print(f"Verifying {data.transaction_id}: {data.amount}")
        return VerifyOutSchema(
            verified=bool(True),
        )

    def after_pay(self, data: AfterPaySchema) -> None:
        print(f"After paying {data.transaction_id}: {data.amount} with tracking code: {data.tracking_code}")

