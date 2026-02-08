import uuid
import requests
from gateways.behpardakht_gateway.datamodel.behpardakht_info_datamodel import BehpardakhtInfoDataModel
from gateways.behpardakht_gateway.datamodel.behpardakht_transaction_datamodel import GatewayTransactionDataModel
from gateways.behpardakht_gateway.schema.pay_schema import PaySchema
from gateways.behpardakht_gateway.schema.after_pay_schema import AfterPaySchema
from gateways.behpardakht_gateway.schema.verify_schema import VerifySchema
from lib.gateway.base_payment_gateway import BasePaymentGateway
from lib.gateway.schema.pay_out_schema import PayOutSchema
from lib.gateway.schema.verify_out_schema import VerifyOutSchema
from time import gmtime, strftime
from zeep import Client, Transport
from zeep.exceptions import Fault


class BehpardakhtGateway(BasePaymentGateway):

    def pay(self, info: BehpardakhtInfoDataModel, data: PaySchema) -> PayOutSchema:
        data = {
            "terminalId": int(info.get('terminal_id')),
            "userName": info.get('username'),
            "userPassword": info.get('password'),
            "orderId": data.get('transaction_id'),
            "amount": data.get('amount'),
            "localDate": self.get_current_date(),
            "localTime": self.get_current_time(),
            "additionalData": data.get('description'),
            "callBackUrl": data.get('call_back_url'),
            "mobileNo": data.get('mobile_number'),
            "payerId": data.get('payment_id')
        }

        try:
            client = self.get_client()
        except requests.ConnectTimeout as e:
            return "در ارتباط با بانک مشکلی پیش آمده است.", None

        try:
            response = client.service.bpPayRequest(**data)
            parts = response.split(",")
            status, token = parts
            if len(parts) != 2:
                return "پاسخ نامعتبر از بانک دریافت شد.", None
            if status == "0":
                return PayOutSchema(
                    url=f"{self.default_urls()['start_pay_url']}?RefId={token}",
                    transaction_id=str(uuid)
                )
            else:
                return self.get_status_message(status), None
        except requests.ConnectTimeout as e:
            return "در ارتباط با بانک مشکلی پیش آمده است.", None

        except (Fault, ValueError) as e:
            return "در ارتباط با بانک مشکلی پیش آمده است.", None

    def verify(self, info: BehpardakhtInfoDataModel, data: VerifySchema) -> VerifyOutSchema:
        print(f"Verifying {data.transaction_id}: {data.amount}")
        data = {
            "terminalId": info.get('terminal_id'),
            "userName": info.get('username'),
            "userPassword": info.get('password'),
            "orderId": data.get('transaction_id'),
            "saleOrderId": data.get('transaction_id'),
            "saleReferenceId": data.get('sale_reference_id'),
        }

        client = self.get_client()
        verify_result = client.service.bpVerifyRequest(**data)

        if verify_result == "0":
            return VerifyOutSchema(
                verified=self.settle_payment(data),
            )
        elif verify_result == "45" or verify_result == 45:
            return VerifyOutSchema(
                verified=True,
            )
        else:
            inquiry_result = client.service.bpInquiryRequest(**data)
            if inquiry_result == "0":
                return VerifyOutSchema(
                    verified=True,
                )
            else:
                reversal_result = client.service.bpReversalRequest(**data)
                return VerifyOutSchema(
                    verified=False,
                )

    def after_pay(self, data: AfterPaySchema) -> GatewayTransactionDataModel:
        res_code = data.get('resCode')
        sale_reference_id = data.get('SaleReferenceId')
        order_id = data.get('SaleOrderId')
        card_number = data.get('CardHolderPan')
        ref_id = data.get('RefId')

        return GatewayTransactionDataModel(
            res_code=res_code,
            sale_reference_id=sale_reference_id,
            order_id=order_id,
            card_number=card_number,
            ref_id=ref_id
        )

    @staticmethod
    def default_urls():
        return {
            'payment_wsdl': 'https://bpm.shaparak.ir/pgwchannel/services/pgw?wsdl',
            'start_pay_url': 'https://bpm.shaparak.ir/pgwchannel/startpay.mellat',
        }

    def get_client(self):
        transport = Transport(timeout=5, operation_timeout=10)
        return Client(self.default_urls()['payment_wsdl'], transport=transport)

    @staticmethod
    def get_current_date():
        return strftime("%Y%m%d", gmtime())

    @staticmethod
    def get_current_time():
        return strftime("%H%M%S")

    def settle_payment(self, data: dict):
        client = self.get_client()
        result = client.service.bpSettleRequest(**data)

        if result == "0" or result == 0:
            return True
        elif result == "45" or result == 45:
            return True
        else:
            return False

    @staticmethod
    def get_status_message(code: str) -> str:
        return messages.get(code, "خطای نامشخص")