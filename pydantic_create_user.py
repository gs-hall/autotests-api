"""Pydantic-модели для POST /api/v1/users."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    """Модель данных пользователя из ответа API."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserRequestSchema(BaseModel):
    """Модель запроса на создание пользователя."""

    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserResponseSchema(BaseModel):
    """Модель ответа на создание пользователя."""

    user: UserSchema
