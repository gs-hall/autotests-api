from pydantic import BaseModel, Field, EmailStr, ConfigDict
from tools.fakers import fake

class UserSchema(BaseModel):
    """
    Описание структуры пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr = Field(default_factory=fake.email)
    last_name: str = Field(validation_alias="lastName", serialization_alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(validation_alias="firstName", serialization_alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(validation_alias="middleName", serialization_alias="middleName", default_factory=fake.middle_name)


class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(validation_alias="lastName", serialization_alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(validation_alias="firstName", serialization_alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(validation_alias="middleName", serialization_alias="middleName", default_factory=fake.middle_name)


class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserSchema


class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr = Field(default_factory=fake.email)
    last_name: str | None = Field(default_factory=fake.last_name, validation_alias="lastName", serialization_alias="lastName")
    first_name: str | None = Field(default_factory=fake.first_name, validation_alias="firstName", serialization_alias="firstName")
    middle_name: str | None = Field(default_factory=fake.middle_name, validation_alias="middleName", serialization_alias="middleName")


class UpdateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления пользователя.
    """
    user: UserSchema


class GetUserResponseSchema(BaseModel):
    """
    Описание структуры запроса получения пользователя.
    """
    user: UserSchema
