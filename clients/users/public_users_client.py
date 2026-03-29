from typing import TypedDict

import httpx

from clients.api_client import APIClient


class CreateUserRequestDict(TypedDict):
    """Структура тела запроса для создания пользователя."""

    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(APIClient):
    """Клиент для публичных методов /api/v1/users, не требующих авторизации."""

    def create_user_api(self, request: CreateUserRequestDict) -> httpx.Response:
        """Создает пользователя через POST /api/v1/users.

        :param request: Словарь с данными пользователя.
                        Обязательные поля: email, password, lastName, firstName, middleName.
        :return: Ответ сервера в формате httpx.Response.
        """

        return self.post("/api/v1/users", json=request)
