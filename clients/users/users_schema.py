from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserSchema(BaseModel):
    """
    Описание структуры пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(validation_alias="lastName", serialization_alias="lastName")
    first_name: str = Field(validation_alias="firstName", serialization_alias="firstName")
    middle_name: str = Field(validation_alias="middleName", serialization_alias="middleName")


class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    password: str
    last_name: str = Field(validation_alias="lastName", serialization_alias="lastName")
    first_name: str = Field(validation_alias="firstName", serialization_alias="firstName")
    middle_name: str = Field(validation_alias="middleName", serialization_alias="middleName")


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

    email: EmailStr | None
    last_name: str | None = Field(default=None, validation_alias="lastName", serialization_alias="lastName")
    first_name: str | None = Field(default=None, validation_alias="firstName", serialization_alias="firstName")
    middle_name: str | None = Field(default=None, validation_alias="middleName", serialization_alias="middleName")


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
