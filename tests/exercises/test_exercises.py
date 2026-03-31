import pytest
from http import HTTPStatus
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, assert_update_exercise_response

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

    def test_update_exercise(self, exercises_client, function_exercise):
        """
        Проверяет обновление задания через PATCH /api/v1/exercises/{exercise_id}.
        """
        from clients.exercises.exercises_schema import UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
        from tools.assertions.exercises import assert_update_exercise_response
        from tools.assertions.base import assert_status_code
        from tools.assertions.schema import validate_json_schema
        exercise_id = function_exercise.response.exercise.id
        # Сгенерируем новый запрос на обновление (можно использовать фабрику или явно)
        update_request = UpdateExerciseRequestSchema(course_id=function_exercise.response.exercise.course_id)
        response = exercises_client.update_exercise_api(exercise_id, update_request)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(update_request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(self, exercises_client, function_exercise):
        """
        Проверяет удаление задания через DELETE /api/v1/exercises/{exercise_id} и отсутствие задания после удаления.
        """
        exercise_id = function_exercise.response.exercise.id
        # Удаляем задание
        delete_response = exercises_client.delete_exercise_api(exercise_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # Пробуем получить удалённое задание
        get_response = exercises_client.get_exercise_api(exercise_id)
        from clients.errors_schema import InternalErrorResponseSchema
        from tools.assertions.exercises import assert_exercise_not_found_response
        error_data = InternalErrorResponseSchema.model_validate_json(get_response.text)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(error_data)
        validate_json_schema(get_response.json(), error_data.model_json_schema())
