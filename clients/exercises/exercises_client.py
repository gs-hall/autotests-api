from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class GetExercisesQueryDict(TypedDict):
    """Описание структуры query-параметров для получения списка заданий."""

    courseId: str


class CreateExerciseRequestDict(TypedDict):
    """Описание структуры запроса на создание задания."""

    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    courseId: str


class UpdateExerciseRequestDict(TypedDict):
    """Описание структуры запроса на обновление задания."""

    title: str | None
    maxScore: int | None
    minScore: int | None
    description: str | None
    estimatedTime: str | None


class ExercisesClient(APIClient):
    """Клиент для работы с /api/v1/exercises."""

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """Получает список заданий для указанного курса.

        :param query: Словарь с query-параметром courseId.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        params = {"courseId": query["courseId"]}
        return self.get("/api/v1/exercises", params=params)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """Получает информацию о задании по его идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """Создает новое задание.

        :param request: Словарь с данными задания.
                        Обязательные поля: title, maxScore, minScore,
                        description, estimatedTime, courseId.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """Обновляет данные задания по идентификатору.

        :param exercise_id: Идентификатор задания.
        :param request: Словарь с полями для частичного обновления.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """Удаляет задание по идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        return self.delete(f"/api/v1/exercises/{exercise_id}")
