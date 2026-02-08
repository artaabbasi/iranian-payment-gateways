from pydantic import BaseModel


class BehpardakhtInfoDataModel(BaseModel):
    username: str
    password: str
    terminal_id: int
