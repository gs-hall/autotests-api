"""Pydantic-схемы для API /api/v1/exercises."""

from pydantic import BaseModel, ConfigDict, Field

from tools.fakers import fake


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

    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(
        validation_alias="courseId",
        serialization_alias="courseId",
        default_factory=fake.uuid4,
    )
    max_score: int = Field(
        validation_alias="maxScore",
        serialization_alias="maxScore",
        default_factory=fake.max_score,
    )
    min_score: int = Field(
        validation_alias="minScore",
        serialization_alias="minScore",
        default_factory=fake.min_score,
    )
    order_index: int = Field(
        validation_alias="orderIndex",
        serialization_alias="orderIndex",
        default_factory=fake.integer,
    )
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(
        validation_alias="estimatedTime",
        serialization_alias="estimatedTime",
        default_factory=fake.estimated_time,
    )


class CreateExerciseResponseSchema(BaseModel):
    """Модель ответа на создание задания."""

    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    """Модель запроса на обновление задания."""

    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default_factory=fake.sentence)
    course_id: str | None = Field(
        default_factory=fake.uuid4,
        validation_alias="courseId",
        serialization_alias="courseId",
    )
    max_score: int | None = Field(
        default_factory=fake.max_score,
        validation_alias="maxScore",
        serialization_alias="maxScore",
    )
    min_score: int | None = Field(
        default_factory=fake.min_score,
        validation_alias="minScore",
        serialization_alias="minScore",
    )
    order_index: int | None = Field(
        default_factory=fake.integer,
        validation_alias="orderIndex",
        serialization_alias="orderIndex",
    )
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(
        default_factory=fake.estimated_time,
        validation_alias="estimatedTime",
        serialization_alias="estimatedTime",
    )


class UpdateExerciseResponseSchema(BaseModel):
    """Модель ответа на обновление задания."""

    exercise: ExerciseSchema
