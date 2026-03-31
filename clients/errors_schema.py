from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class ValidationErrorSchema(BaseModel):
    """
    Модель, описывающая структуру ошибки валидации API.
    """
    model_config = ConfigDict(populate_by_name=True)

    type: str
    input: Any
    context: dict[str, Any] = Field(validation_alias="ctx", serialization_alias="ctx")
    message: str = Field(validation_alias="msg", serialization_alias="msg")
    location: list[str] = Field(validation_alias="loc", serialization_alias="loc")


class ValidationErrorResponseSchema(BaseModel):
    """
    Модель, описывающая структуру ответа API с ошибкой валидации.
    """
    model_config = ConfigDict(populate_by_name=True)

    details: list[ValidationErrorSchema] = Field(validation_alias="detail", serialization_alias="detail")

class InternalErrorResponseSchema(BaseModel):
    """
    Модель для описания внутренней ошибки.
    """

    model_config = ConfigDict(populate_by_name=True)

    details: str = Field(validation_alias="detail", serialization_alias="detail")
