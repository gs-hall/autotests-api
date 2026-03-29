# Run:
# /Users/e.ivantsov/code/python/autotests-api/.venv/bin/python httpx_exercises_client_example.py

import json
import sys
from base64 import urlsafe_b64decode

import httpx

from clients.exercises.exercises_client import ExercisesClient


BASE_URL = "http://localhost:8000"
EMAIL = "user@example.com"
PASSWORD = "string"
COURSE_ID = "4da3bf55-17f7-43fb-b9c4-97ed26acb690"


def decode_user_id_from_token(access_token: str) -> str | None:
    parts = access_token.split(".")
    if len(parts) != 3:
        return None

    payload_part = parts[1]
    padding = "=" * (-len(payload_part) % 4)

    try:
        decoded_payload = urlsafe_b64decode(f"{payload_part}{padding}").decode("utf-8")
        payload_data = json.loads(decoded_payload)
    except (ValueError, json.JSONDecodeError):
        return None

    user_id = payload_data.get("user_id")
    return user_id if isinstance(user_id, str) else None


def resolve_course_id(client: httpx.Client, access_token: str) -> str | None:
    if COURSE_ID != "replace-with-real-course-id":
        return COURSE_ID

    user_id = decode_user_id_from_token(access_token)
    if not user_id:
        return None

    courses_response = client.get("/api/v1/courses", params={"userId": user_id})
    if courses_response.status_code != 200:
        return None

    try:
        courses_data = courses_response.json()
    except json.JSONDecodeError:
        return None

    courses_list = courses_data if isinstance(courses_data, list) else courses_data.get("courses")
    if not isinstance(courses_list, list) or not courses_list:
        return None

    first_course = courses_list[0]
    if not isinstance(first_course, dict):
        return None

    course_id = first_course.get("id")
    return course_id if isinstance(course_id, str) else None


def main() -> int:
    login_payload = {
        "email": EMAIL,
        "password": PASSWORD,
    }
    login_response = httpx.post(f"{BASE_URL}/api/v1/authentication/login", json=login_payload)
    print(f"Login status code: {login_response.status_code}")

    if login_response.status_code != 200:
        print(json.dumps(login_response.json(), ensure_ascii=False, indent=2))
        return 1

    access_token = login_response.json()["token"]["accessToken"]

    with httpx.Client(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    ) as httpx_client:
        course_id = resolve_course_id(httpx_client, access_token)
        if not course_id:
            print("Could not resolve course ID automatically. Set COURSE_ID in the script.")
            return 1

        exercises_client = ExercisesClient(httpx_client)
        exercises_response = exercises_client.get_exercises_api({"courseId": course_id})

    print(f"Get exercises status code: {exercises_response.status_code}")
    print(json.dumps(exercises_response.json(), ensure_ascii=False, indent=2))

    return 0 if exercises_response.status_code == 200 else 1


if __name__ == "__main__":
    sys.exit(main())