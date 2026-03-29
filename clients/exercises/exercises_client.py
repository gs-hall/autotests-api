from typing import TypedDict

from httpx import QueryParams, Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class Exercise(TypedDict):
    """Описание структуры задания."""

    id: str
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class GetExercisesQueryDict(TypedDict):
    """Описание структуры query-параметров для получения списка заданий."""

    courseId: str


class GetExercisesResponseDict(TypedDict):
    """Описание структуры ответа получения списка заданий."""

    exercises: list[Exercise]


class GetExerciseResponseDict(TypedDict):
    """Описание структуры ответа получения задания."""

    exercise: Exercise


class CreateExerciseRequestDict(TypedDict):
    """Описание структуры запроса на создание задания."""

    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    courseId: str


class CreateExerciseResponseDict(TypedDict):
    """Описание структуры ответа создания задания."""

    exercise: Exercise


class UpdateExerciseRequestDict(TypedDict):
    """Описание структуры запроса на обновление задания."""

    title: str | None
    maxScore: int | None
    minScore: int | None
    description: str | None
    estimatedTime: str | None


class UpdateExerciseResponseDict(TypedDict):
    """Описание структуры ответа обновления задания."""

    exercise: Exercise


class ExercisesClient(APIClient):
    """Клиент для работы с /api/v1/exercises."""

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """Получает список заданий для указанного курса.

        :param query: Словарь с query-параметром courseId.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """

        return self.get("/api/v1/exercises", params=QueryParams(**query))

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

    def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
        """Получает список заданий и возвращает JSON-ответ.

        :param query: Словарь с query-параметром courseId.
        :return: JSON-ответ в формате GetExercisesResponseDict.
        """

        response = self.get_exercises_api(query)
        return response.json()

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseDict:
        """Получает задание по идентификатору и возвращает JSON-ответ.

        :param exercise_id: Идентификатор задания.
        :return: JSON-ответ в формате GetExerciseResponseDict.
        """

        response = self.get_exercise_api(exercise_id)
        return response.json()

    def create_exercise(self, request: CreateExerciseRequestDict) -> CreateExerciseResponseDict:
        """Создает задание и возвращает JSON-ответ.

        :param request: Словарь с данными задания.
        :return: JSON-ответ в формате CreateExerciseResponseDict.
        """

        response = self.create_exercise_api(request)
        return response.json()

    def update_exercise(
            self,
            exercise_id: str,
            request: UpdateExerciseRequestDict
    ) -> UpdateExerciseResponseDict:
        """Обновляет задание и возвращает JSON-ответ.

        :param exercise_id: Идентификатор задания.
        :param request: Словарь с полями для частичного обновления.
        :return: JSON-ответ в формате UpdateExerciseResponseDict.
        """

        response = self.update_exercise_api(exercise_id, request)
        return response.json()


def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
    """Создает экземпляр ExercisesClient с приватным HTTP-клиентом.

    :param user: Данные пользователя для аутентификации.
    :return: Готовый к использованию ExercisesClient.
    """

    return ExercisesClient(client=get_private_http_client(user))

