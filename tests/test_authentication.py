from http import HTTPStatus

from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.authentication.authentication_client import get_authentication_client
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response


def test_login():
    """
    Тест проверяет процесс аутентификации пользователя.

    Посредством:
    1. Создания нового пользователя
    2. Выполнения аутентификации с его учетными данными
    3. Проверки статус-кода (200)
    4. Валидации структуры ответа
    5. Проверки наличия токенов и их типов
    """
    # Инициализируем клиентов
    public_users_client = get_public_users_client()
    authentication_client = get_authentication_client()

    # Создаем нового пользователя
    create_user_request = CreateUserRequestSchema()
    create_user_response = public_users_client.create_user_api(create_user_request)
    user_data = CreateUserResponseSchema.model_validate_json(create_user_response.text)

    # Выполняем аутентификацию с учетными данными созданного пользователя
    login_request = LoginRequestSchema(
        email=create_user_request.email,
        password=create_user_request.password
    )
    login_response = authentication_client.login_api(login_request)

    # Проверяем статус-код ответа (200)
    assert_status_code(login_response.status_code, HTTPStatus.OK)

    # Десериализуем JSON-ответ в LoginResponseSchema
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    # Проверяем корректность тела ответа
    assert_login_response(login_response_data)
