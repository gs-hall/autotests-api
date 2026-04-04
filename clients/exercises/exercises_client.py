import allure
from httpx import QueryParams, Response

from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
)
from clients.private_http_builder import (
    AuthenticationUserSchema,
    get_private_http_client,
)
from tools.routes import APIRoutes


class ExercisesClient(APIClient):
    """Клиент для работы с /api/v1/exercises."""

    @allure.step("Get exercises")
    @tracker.track_coverage_httpx(APIRoutes.EXERCISES)
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """Получает список заданий для указанного курса.

        :param query: Модель query-параметров с course_id.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(
            APIRoutes.EXERCISES, params=QueryParams(**query.model_dump(by_alias=True))
        )

    @allure.step("Get exercise by id {exercise_id}")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def get_exercise_api(self, exercise_id: str) -> Response:
        """Получает информацию о задании по его идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Create exercise")
    @tracker.track_coverage_httpx(APIRoutes.EXERCISES)
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """Создает новое задание.

        :param request: Модель запроса на создание задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(APIRoutes.EXERCISES, json=request.model_dump(by_alias=True))

    @allure.step("Update exercise by id {exercise_id}")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def update_exercise_api(
        self, exercise_id: str, request: UpdateExerciseRequestSchema
    ) -> Response:
        """Обновляет данные задания по идентификатору.

        :param exercise_id: Идентификатор задания.
        :param request: Модель запроса на частичное обновление.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.patch(
            f"{APIRoutes.EXERCISES}/{exercise_id}",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )

    @allure.step("Delete exercise by id {exercise_id}")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """Удаляет задание по идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        return self.delete(f"{APIRoutes.EXERCISES}/{exercise_id}")

    def get_exercises(
        self, query: GetExercisesQuerySchema
    ) -> GetExercisesResponseSchema:
        """Получает список заданий и возвращает JSON-ответ.

        :param query: Модель query-параметров с course_id.
        :return: Ответ в формате GetExercisesResponseSchema.
        """
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        """Получает задание по идентификатору и возвращает JSON-ответ.

        :param exercise_id: Идентификатор задания.
        :return: Ответ в формате GetExerciseResponseSchema.
        """
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def create_exercise(
        self, request: CreateExerciseRequestSchema
    ) -> CreateExerciseResponseSchema:
        """Создает задание и возвращает JSON-ответ.

        :param request: Модель запроса на создание задания.
        :return: Ответ в формате CreateExerciseResponseSchema.
        """
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(
        self, exercise_id: str, request: UpdateExerciseRequestSchema
    ) -> UpdateExerciseResponseSchema:
        """Обновляет задание и возвращает JSON-ответ.

        :param exercise_id: Идентификатор задания.
        :param request: Модель запроса на частичное обновление.
        :return: Ответ в формате UpdateExerciseResponseSchema.
        """
        response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """Создает экземпляр ExercisesClient с приватным HTTP-клиентом.

    :param user: Данные пользователя для аутентификации.
    :return: Готовый к использованию ExercisesClient.
    """

    return ExercisesClient(client=get_private_http_client(user))
