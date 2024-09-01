import uuid

from sqlalchemy import Column, Integer, TIMESTAMP, func, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base

class Notes(Base):
    __tablename__ = 'Notes'

    UUID = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, nullable=False, index = True)
    text = Column(Text, nullable = False)
    created_at = Column(TIMESTAMP, server_default=func.now())

