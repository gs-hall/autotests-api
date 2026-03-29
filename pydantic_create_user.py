"""Pydantic-модели для POST /api/v1/users."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from tools.fakers import fake


class UserSchema(BaseModel):
    """Модель данных пользователя из ответа API."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr = Field(default_factory=fake.email)
    last_name: str = Field(validation_alias="lastName", serialization_alias="lastName")
    first_name: str = Field(validation_alias="firstName", serialization_alias="firstName")
    middle_name: str = Field(validation_alias="middleName", serialization_alias="middleName")


class CreateUserRequestSchema(BaseModel):
    """Модель запроса на создание пользователя."""

    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(validation_alias="lastName", serialization_alias="lastName")
    first_name: str = Field(validation_alias="firstName", serialization_alias="firstName")
    middle_name: str = Field(validation_alias="middleName", serialization_alias="middleName")


class CreateUserResponseSchema(BaseModel):
    """Модель ответа на создание пользователя."""

    user: UserSchema
