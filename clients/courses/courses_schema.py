"""Pydantic-схемы для API /api/v1/courses."""

from pydantic import BaseModel, ConfigDict, Field

from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema

from tools.fakers import fake


class CourseSchema(BaseModel):
    """Модель данных курса."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int = Field(validation_alias="maxScore", serialization_alias="maxScore")
    min_score: int = Field(validation_alias="minScore", serialization_alias="minScore")
    description: str
    preview_file: FileSchema = Field(validation_alias="previewFile", serialization_alias="previewFile")
    estimated_time: str = Field(validation_alias="estimatedTime", serialization_alias="estimatedTime")
    created_by_user: UserSchema = Field(validation_alias="createdByUser", serialization_alias="createdByUser")


class GetCoursesQuerySchema(BaseModel):
    """Модель query-параметров для получения списка курсов."""

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(validation_alias="userId", serialization_alias="userId")


class GetCoursesResponseSchema(BaseModel):
    """Модель ответа со списком курсов."""

    courses: list[CourseSchema]


class GetCourseResponseSchema(BaseModel):
    """Модель ответа с одним курсом."""

    course: CourseSchema


class CreateCourseRequestSchema(BaseModel):
    """Модель запроса на создание курса."""

    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(validation_alias="maxScore", serialization_alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(validation_alias="minScore", serialization_alias="minScore", default_factory=fake.min_score)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(validation_alias="estimatedTime", serialization_alias="estimatedTime", default_factory=fake.estimated_time)
    preview_file_id: str = Field(validation_alias="previewFileId", serialization_alias="previewFileId", default_factory=fake.uuid4)
    created_by_user_id: str = Field(validation_alias="createdByUserId", serialization_alias="createdByUserId", default_factory=fake.uuid4)


class CreateCourseResponseSchema(BaseModel):
    """Модель ответа на создание курса."""

    course: CourseSchema


class UpdateCourseRequestSchema(BaseModel):
    """Модель запроса на обновление курса."""

    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(default_factory=fake.max_score, validation_alias="maxScore", serialization_alias="maxScore")
    min_score: int | None = Field(default_factory=fake.min_score, validation_alias="minScore", serialization_alias="minScore")
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(default_factory=fake.estimated_time, validation_alias="estimatedTime", serialization_alias="estimatedTime")


class UpdateCourseResponseSchema(BaseModel):
    """Модель ответа на обновление курса."""

    course: CourseSchema
