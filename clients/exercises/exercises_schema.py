"""Pydantic-схемы для API /api/v1/exercises."""

from pydantic import BaseModel, ConfigDict, Field


class ExerciseSchema(BaseModel):
    """Модель данных задания."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(validation_alias="courseId", serialization_alias="courseId")
    max_score: int = Field(validation_alias="maxScore", serialization_alias="maxScore")
    min_score: int = Field(validation_alias="minScore", serialization_alias="minScore")
    order_index: int = Field(validation_alias="orderIndex", serialization_alias="orderIndex")
    description: str
    estimated_time: str = Field(validation_alias="estimatedTime", serialization_alias="estimatedTime")


class GetExercisesQuerySchema(BaseModel):
    """Модель query-параметров для получения списка заданий."""

    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(validation_alias="courseId", serialization_alias="courseId")


class GetExercisesResponseSchema(BaseModel):
    """Модель ответа со списком заданий."""

    exercises: list[ExerciseSchema]


class GetExerciseResponseSchema(BaseModel):
    """Модель ответа с одним заданием."""

    exercise: ExerciseSchema


class CreateExerciseRequestSchema(BaseModel):
    """Модель запроса на создание задания."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(validation_alias="courseId", serialization_alias="courseId")
    max_score: int = Field(validation_alias="maxScore", serialization_alias="maxScore")
    min_score: int = Field(validation_alias="minScore", serialization_alias="minScore")
    description: str
    estimated_time: str = Field(validation_alias="estimatedTime", serialization_alias="estimatedTime")


class CreateExerciseResponseSchema(BaseModel):
    """Модель ответа на создание задания."""

    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    """Модель запроса на обновление задания."""

    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    max_score: int | None = Field(default=None, validation_alias="maxScore", serialization_alias="maxScore")
    min_score: int | None = Field(default=None, validation_alias="minScore", serialization_alias="minScore")
    description: str | None = None
    estimated_time: str | None = Field(default=None, validation_alias="estimatedTime", serialization_alias="estimatedTime")


class UpdateExerciseResponseSchema(BaseModel):
    """Модель ответа на обновление задания."""

    exercise: ExerciseSchema
