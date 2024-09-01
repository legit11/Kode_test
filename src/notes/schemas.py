import datetime
from uuid import UUID
from pydantic import BaseModel


class Note(BaseModel):
    UUID: UUID
    user_id: int
    text: str
    created_at: datetime.datetime