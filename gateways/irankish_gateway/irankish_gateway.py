from gateways.irankish_gateway.datamodel.irankish_info_datamodel import IranKishInfoDataModel
from gateways.irankish_gateway.datamodel.irankish_transaction_datamodel import GatewayTransactionDataModel
from gateways.irankish_gateway.exceptions import messages
from gateways.irankish_gateway.schema.pay_schema import PaySchema
from gateways.irankish_gateway.schema.after_pay_schema import AfterPaySchema
from gateways.irankish_gateway.schema.verify_schema import VerifySchema
from lib.gateway.base_exception import GatewayError, GatewayConnectionError
from lib.gateway.base_payment_gateway import BasePaymentGateway
from lib.gateway.schema.pay_out_schema import PayOutSchema
from lib.gateway.schema.verify_out_schema import VerifyOutSchema
import datetime
import os
import pytz
import requests
import rsa
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad


class IranKishGateway(BasePaymentGateway):
    def __init__(self , info: IranKishInfoDataModel):
        super().__init__(info)

    @staticmethod
    def _get_status_message(code: str) -> str:
        return messages.get(code, "خطای نامشخص")

    def _load_rsa_public_key(self):
        try:
            path = self._info.rsa_public_key_file_path

            if not path:
                raise ValueError("RSA public key path is not set")

            with open(path, "rb") as f:
                rsa_public_key_data = f.read()

            rsa_public_key = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_public_key_data)
            return rsa_public_key

        except FileNotFoundError:
            raise FileNotFoundError(f"❌ RSA public key file for IranKishGateway not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to load RSA public key: {e}") from e

    @staticmethod
    def _iran_kish_default_urls():
        iran_kish_urls = {
            'get_token_url': 'https://ikc.shaparak.ir/api/v3/tokenization/make',
            'post_and_redirect_url': 'https://ikc.shaparak.ir/iuiv3/IPG/Index/',
            'confirmation_url': 'https://ikc.shaparak.ir/api/v3/confirmation/purchase'
        }
        return iran_kish_urls

    def pay(self, data: PaySchema) -> PayOutSchema:
        aes_key, aes_iv = os.urandom(16), os.urandom(16)
        aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        byte_array_data = bytearray(48)
        byte_array_data[0:16], byte_array_data[16:48] = aes_key, \
            bytearray(
                SHA256.new(
                    aes.encrypt(
                        pad(
                            bytes(
                                bytearray.fromhex(
                                    self._info.terminal_id +
                                    self._info.pass_phrase +
                                    str(data.amount).zfill(12) +
                                    '00'
                                )
                            ),
                            16
                        )
                    )
                ).digest()
            )
        authentication_envelope = {
            'iv': aes_iv.hex(),
            'data': rsa.encrypt(byte_array_data, self._load_rsa_public_key()).hex()
        }
        request = {
            'transactionType': 'Purchase',
            'terminalId': self._info.terminal_id,
            'acceptorId': self._info.acceptor_id,
            'paymentId': self._info.payment_id,
            'amount': data.amount,
            'revertUri': data.call_back_url,
            'requestId': data.transaction_id,
            'requestTimestamp': int(datetime.datetime.timestamp(datetime.datetime.now(tz=pytz.UTC)))
        }

        payload = {
            'authenticationEnvelope': authentication_envelope,
            'request': request
        }
        try:
            r = requests.post(self._iran_kish_default_urls().get('get_token_url'), json=payload, verify=False)
        except Exception as e:
            raise GatewayConnectionError("ارتباط با درگاه قطع میباشد.")

        if r.ok:
            result = r.json()
            if result['responseCode'] == '00':
                return PayOutSchema(
                    url=self._iran_kish_default_urls().get('post_and_redirect_url'),
                    transaction_id=data.transaction_id,
                    token=result['result']['token']
                )

        result = r.json()
        raise GatewayError(code=result['responseCode'], text=self._get_status_message(result['responseCode']))

    def verify(self, data: VerifySchema) -> VerifyOutSchema:
        if data.res_code == '00':
            payload = {
                'terminalId': data.terminal_id,
                'retrievalReferenceNumber': data.reference_id,
                'systemTraceAuditNumber': data.tracking_code,
                'tokenidentity': data.token,
            }
            r = requests.post(self._iran_kish_default_urls().get('confirmation_url'), json=payload, verify=False)
            if r.ok:
                result = r.json()
                if result['status']:
                    return VerifyOutSchema(verified=True,)
                else:
                    return VerifyOutSchema(verified=False,)
            return VerifyOutSchema(verified=False,)
        return VerifyOutSchema(verified=False,)

    def after_pay(self, data: AfterPaySchema) -> GatewayTransactionDataModel:
        res_code = data.responseCode
        sale_reference_id = data.retrievalReferenceNumber
        order_id = data.requestId
        card_number = data.maskedPan
        ref_id = data.systemTraceAuditNumber
        token = data.token
        merchant_id = data.merchantID

        return GatewayTransactionDataModel(
            res_code=res_code,
            sale_reference_id=sale_reference_id,
            order_id=order_id,
            card_number=card_number,
            ref_id=ref_id,
            token=token,
            merchant_id=merchant_id,
        )
