import pytest
from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from typing import Any

class ExerciseFixture:
    """
    Агрегатор данных о созданном задании для тестов.
    """
    def __init__(self, request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
        self.request = request
        self.response = response

@pytest.fixture(scope="function")
def exercises_client(function_user) -> ExercisesClient:
    """
    Возвращает экземпляр ExercisesClient для работы с API заданий.
    """
    return get_exercises_client(function_user.authentication_user)

@pytest.fixture(scope="function")
def function_exercise(function_course, exercises_client: ExercisesClient) -> ExerciseFixture:
    """
    Создаёт тестовое задание и возвращает агрегатор ExerciseFixture.
    """
    request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
    response = exercises_client.create_exercise(request)
    return ExerciseFixture(request=request, response=response)
