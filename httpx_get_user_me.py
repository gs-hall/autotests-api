# Run:
# python3 httpx_get_user_me.py --base-url http://localhost:8000 --email user@example.com --password string

import argparse
import json
import sys

import httpx


LOGIN_PATH = "/api/v1/authentication/login"
USER_ME_PATH = "/api/v1/users/me"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Login via /api/v1/authentication/login and fetch /api/v1/users/me."
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="API base URL. Default: http://localhost:8000",
    )
    parser.add_argument("--email", required=True, help="User email for authentication")
    parser.add_argument("--password", required=True, help="User password for authentication")
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Request timeout in seconds. Default: 10",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        with httpx.Client(timeout=args.timeout) as client:
            access_token = login(client, args.base_url, args.email, args.password)
            response = get_current_user(client, args.base_url, access_token)
    except httpx.HTTPError as exc:
        print(f"Request failed: {exc}")
        return 1

    print(f"Status code: {response.status_code}")
    print_response_body(response)

    return 0 if response.status_code == 200 else 1


if __name__ == "__main__":
    sys.exit(main())