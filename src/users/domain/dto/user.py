from datetime import datetime

from pydantic import EmailStr, validator

from core.dto import BaseInSchema, BaseOutSchema
from users.enums import BustType
from users.utils import validate_url, validate_phone


class UserSchema(BaseOutSchema):
    email: EmailStr | None = None
    phone: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    avatar: str | None = None
    birth_date: datetime | None = None
    uae_id: str | None = None
    passport_id: str | None = None
    street: str | None = None
    city: str | None = None
    country: str | None = None
    state: str | None = None
    instagram_url: str | None = None
    height: float | None = None
    weight: float | None = None
    bust_type: BustType | None = None


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
