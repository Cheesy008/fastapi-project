from datetime import datetime

from pydantic import EmailStr, validator

from core.dto import BaseInSchema, BaseOutSchema, OrmModel
from users.utils import validate_url, validate_phone


class BaseUserSchema(OrmModel):
    email: EmailStr | None = None
    phone: str | None = None
    is_active: bool | None = None
    birth_date: datetime | None = None
    street: str | None = None
    city: str | None = None
    country: str | None = None


class UserOutSchema(BaseOutSchema, BaseUserSchema):
    ...


class UserRegisterInSchema(BaseInSchema):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str
    password_confirmation: str
    redirect_url: str | None = None

    @validator("password_confirmation")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("redirect_url")
    def redirect_url_validation(cls, v):
        return validate_url(v)

    @validator("phone")
    def phone_validation(cls, v):
        return validate_phone(v)


class UserCreateDBSchema(BaseInSchema):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    hashed_password: str
