import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import Field, EmailStr


class UserRead(schemas.BaseUser[int]):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    password: str = Field(..., min_length=5, description="Пароль должен состоять минимум из 5 символов")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

