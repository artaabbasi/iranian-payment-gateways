from pydantic import BaseModel


class VerifyOutSchema(BaseModel):
    verified: bool
