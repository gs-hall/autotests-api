import json
import sys

import httpx


LOGIN_PATH = "/api/v1/authentication/login"
USER_ME_PATH = "/api/v1/users/me"
BASE_URL = "http://localhost:8000"
EMAIL = "user@example.com"
PASSWORD = "string"
TIMEOUT = 10.0


def build_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}{path}"


def login(client: httpx.Client, base_url: str, email: str, password: str) -> str:
    response = client.post(
        build_url(base_url, LOGIN_PATH),
        json={"email": email, "password": password},
    )

    if response.status_code != 200:
        print(f"Login failed with status code: {response.status_code}")
        print_response_body(response)
        raise SystemExit(1)

    response_json = response.json()
    access_token = response_json.get("accessToken")

    if not access_token:
        token_payload = response_json.get("token")
        if isinstance(token_payload, dict):
            access_token = token_payload.get("accessToken")

    if not access_token:
        print("Login response does not contain accessToken")
        print(json.dumps(response_json, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    return access_token


def get_current_user(client: httpx.Client, base_url: str, access_token: str) -> httpx.Response:
    return client.get(
        build_url(base_url, USER_ME_PATH),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def print_response_body(response: httpx.Response) -> None:
    try:
        body = response.json()
    except json.JSONDecodeError:
        print(response.text)
        return

    print(json.dumps(body, ensure_ascii=False, indent=2))


def main() -> int:
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            access_token = login(client, BASE_URL, EMAIL, PASSWORD)
            response = get_current_user(client, BASE_URL, access_token)
    except httpx.HTTPError as exc:
        print(f"Request failed: {exc}")
        return 1

    print(f"Status code: {response.status_code}")
    print_response_body(response)

    return 0 if response.status_code == 200 else 1


if __name__ == "__main__":
    sys.exit(main())