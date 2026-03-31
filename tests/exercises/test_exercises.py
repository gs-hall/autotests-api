import pytest
from http import HTTPStatus
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response

@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    """
    Тесты для проверки создания задания через API.
    """
    def test_create_exercise(self, exercises_client: ExercisesClient, function_course):
        """
        Проверяет создание задания через POST /api/v1/exercises.
        """
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercises_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(self, exercises_client, function_exercise):
        """
        Проверяет получение задания через GET /api/v1/exercises/{exercise_id}.
        """
        exercise_id = function_exercise.response.exercise.id
        response = exercises_client.get_exercise_api(exercise_id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(response_data, function_exercise.response)
        validate_json_schema(response.json(), response_data.model_json_schema())
