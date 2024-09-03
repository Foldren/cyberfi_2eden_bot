from pydantic import BaseModel


class TelegramUser(BaseModel):
    init_data: str
