from pydantic import BaseModel


class PayOutSchema(BaseModel):
    url: str
    transaction_id: str
