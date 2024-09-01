from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, TIMESTAMP, String, Boolean, func
from src.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    registered_at = Column(TIMESTAMP, server_default=func.now())
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)