# Run:
# python3 httpx_update_user.py

import json
import sys

import httpx

from tools.fakers import fake


BASE_URL = "http://localhost:8000"
PASSWORD = "string"


def print_response(label: str, response: httpx.Response) -> None:
    print(f"{label} status code: {response.status_code}")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


def create_user(client: httpx.Client) -> dict:
    payload = {
        "email": fake.email(),
        "password": PASSWORD,
        "lastName": "string",
        "firstName": "string",
        "middleName": "string",
    }
    response = client.post(f"{BASE_URL}/api/v1/users", json=payload)
    print_response("Create user", response)

    if response.status_code != 200:
        raise SystemExit(1)

    response_data = response.json()
    return {
        "id": response_data["user"]["id"],
        "email": payload["email"],
        "password": payload["password"],
    }


def login(client: httpx.Client, email: str, password: str) -> str:
    payload = {
        "email": email,
        "password": password,
    }
    response = client.post(f"{BASE_URL}/api/v1/authentication/login", json=payload)
    print_response("Login", response)

    if response.status_code != 200:
        raise SystemExit(1)

    return response.json()["token"]["accessToken"]


def update_user(client: httpx.Client, user_id: str, access_token: str) -> httpx.Response:
    payload = {
        "email": fake.email(),
        "lastName": "string",
        "firstName": "string",
        "middleName": "string",
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = client.patch(
        f"{BASE_URL}/api/v1/users/{user_id}",
        json=payload,
        headers=headers,
    )
    print_response("Update user", response)
    return response


def main() -> int:
    with httpx.Client() as client:
        created_user = create_user(client)
        access_token = login(client, created_user["email"], created_user["password"])
        update_response = update_user(client, created_user["id"], access_token)

    return 0 if update_response.status_code == 200 else 1


if __name__ == "__main__":
    sys.exit(main())