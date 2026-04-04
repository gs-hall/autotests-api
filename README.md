# autotests-api

Link is <https://github.com/gs-hall/autotests-api>
python -m pytest -m "regression"
python -m pytest --alluredir=./allure-results
python -m pytest -m "regression" --alluredir=./allure-results

# static

allure generate ./allure-results --output=./allure-report

# dynamic

allure serve ./allure-results

# coverage

swagger-coverage-tool save-report

## Quick Checklist

- Schemas are added/updated in `clients/<entity>/<entity>_schema.py` and match Swagger/OpenAPI.
- Client methods use `APIRoutes` (no hardcoded endpoints) and include `@allure.step`.
- Fixtures are typed, reusable, and use `BaseModel` aggregators (`request` + `response`).
- Assertions are extracted to `tools/assertions/<entity>.py`, include `@allure.step` and `logger.info`.
- Tests include status code checks, payload checks, and JSON schema validation.
- Allure hierarchy is complete: `epic/feature/story/parent_suite/suite/sub_suite`.
- No hardcoded file paths or env-specific values; use `settings` from `config.py`.
- Imports are at the top of file; no function-local imports unless strictly needed.
- Targeted tests pass, then `python -m pytest -m "regression"` passes.

## Main Pytest Autotesting Rules

This project uses a consistent test architecture for every API entity (users, files, courses, exercises, authentication).

### Project layers

- `clients`: HTTP API clients and Pydantic request/response models.
- `fixtures`: pytest fixtures that prepare reusable test data and authenticated clients.
- `tests`: test scenarios (positive and negative) grouped by entity.
- `tools/assertions`: reusable assertion helpers with strict field-by-field checks.
- `tools/allure`: helpers for Allure environment metadata.
- `tools/fakers`: generators for random, valid test data.
- `tools/logger`: unified logger factory for assertions and helper modules.

## Entity checklist (what to create for each new endpoint/entity)

For each new entity, add the following components.

### 1) Pydantic schemas

- Create request/response schemas in `clients/<entity>/<entity>_schema.py`.
- Use strict typing (`UUID`, `HttpUrl`, `FilePath`, `DirectoryPath`, `Optional`, etc. when applicable).
- Keep field aliases consistent with API contract (`validation_alias` and `serialization_alias` if needed).

### 2) API client methods

- Add methods in `clients/<entity>/<entity>_client.py`.
- Use `APIRoutes` enum instead of hardcoded endpoints.
- Separate low-level `*_api` calls (return `httpx.Response`) and high-level typed methods (return Pydantic schema via `model_validate_json`).
- Add `@allure.step(...)` for every public API action.

### 3) Fixtures

- Add fixtures in `fixtures/<entity>.py`.
- Use `BaseModel` fixture aggregators (`request` + `response`) instead of manual classes.
- Keep fixture scope default (`function`) unless wider scope is truly required.
- Add explicit fixture type annotations.
- Use values from settings/config for test data paths (no hardcoded file paths).

### 4) Assertion helpers

- Add helpers in `tools/assertions/<entity>.py`.
- Validate all important response fields explicitly.
- Reuse base helpers (`assert_equal`, `assert_status_code`, `assert_length`).
- Add `@allure.step(...)` to assertion functions.
- Initialize module logger via `get_logger("<ENTITY>_ASSERTIONS")` and add `logger.info(...)` in each assertion.

### 5) Tests

- Add tests in `tests/<entity>/test_<entity>.py`.
- Cover CRUD and negative validation cases where applicable.
- Parse response to Pydantic schema before assertions.
- Validate JSON schema with `validate_json_schema`.
- Keep imports at the top of the file.

## Allure conventions

### Class-level annotations

- `@allure.epic(...)`
- `@allure.feature(...)`
- `@allure.parent_suite(...)` must match `epic`.
- `@allure.suite(...)` must match `feature`.

### Test-level annotations

- `@allure.title(...)`
- `@allure.tag(...)`
- `@allure.story(...)`
- `@allure.sub_suite(...)` must match `story`.
- `@allure.severity(...)`

### Step-level annotations

- API client action methods are decorated with `@allure.step`.
- Assertion helper functions are decorated with `@allure.step`.

## Logging rules

- Use `tools.logger.get_logger` to create module logger once.
- Log meaningful checkpoints via `logger.info(...)` inside assertion helpers.
- Avoid noisy logs in tight loops unless they add diagnostic value.

## Faker rules

- Use project faker utilities from `tools.fakers` in schemas/factories.
- Prefer generated valid defaults to reduce boilerplate in tests.
- Override generated values only when a scenario needs specific input.

## Configuration and environment rules

- Keep runtime config in `config.py` based on `pydantic-settings`.
- Read sensitive/runtime values from `.env`.
- For file-based tests, use config values (for example `settings.test_data.image_png_file`) instead of hardcoded paths.
- Keep Allure environment metadata generation in `tools/allure/environment.py`.

## cURL usage rules

- cURL and raw HTTPX scripts are demo/debug helpers only.
- Main test flow must use typed clients + fixtures + assertions.
- If demo scripts upload files, they must also use config-driven paths.

## Test run commands

- Full regression: `python -m pytest -m "regression"`
- With Allure results: `python -m pytest -m "regression" --alluredir=./allure-results`

## Definition of done for new test functionality

- Schemas are typed and aligned with API contract.
- Client methods are added and use `APIRoutes` + `allure.step`.
- Fixtures are typed and reusable.
- Assertions are extracted, logged, and reusable.
- Tests include status code, payload assertions, and JSON schema validation.
- Allure annotations (`epic/feature/story/suite/sub_suite/parent_suite`) are complete.
- Regression suite passes.

## RU: Основные правила API автотестов на pytest

Этот проект использует единый подход для всех сущностей API (users, files, courses, exercises, authentication).

### Слои проекта

- `clients`: HTTP-клиенты и Pydantic-схемы запросов/ответов.
- `fixtures`: pytest-фикстуры для подготовки данных и клиентов.
- `tests`: тестовые сценарии (позитивные и негативные), сгруппированные по сущностям.
- `tools/assertions`: переиспользуемые проверки ответов API.
- `tools/allure`: утилиты для окружения Allure.
- `tools/fakers`: генерация тестовых данных.
- `tools/logger`: единая инициализация логгера.

### Что нужно создать для новой сущности

#### 1. Pydantic-схемы

- Создать схемы в `clients/<entity>/<entity>_schema.py`.
- Использовать строгую типизацию (`UUID`, `HttpUrl`, `FilePath`, `DirectoryPath` и т.д.).
- При необходимости задавать alias-поля в соответствии с API-контрактом.

#### 2. Методы API-клиента

- Добавить методы в `clients/<entity>/<entity>_client.py`.
- Использовать `APIRoutes`, а не строковые хардкоды эндпоинтов.
- Разделять методы:
- `*_api` возвращают `httpx.Response`.
- typed-методы возвращают Pydantic-модель через `model_validate_json`.
- Добавлять `@allure.step(...)` для каждого пользовательского действия в клиенте.

#### 3. Фикстуры

- Добавить фикстуры в `fixtures/<entity>.py`.
- Использовать `BaseModel`-агрегаторы (`request` + `response`).
- Не указывать `scope="function"`, если нужен scope по умолчанию.
- Добавлять аннотации типов у входных фикстур.
- Для тестовых файлов использовать пути из `settings`, без хардкода.

#### 4. Проверки (assertions)

- Добавить проверки в `tools/assertions/<entity>.py`.
- Проверять все значимые поля ответа явно.
- Переиспользовать общие проверки: `assert_equal`, `assert_status_code`, `assert_length`.
- Добавлять `@allure.step(...)` к каждой assertion-функции.
- Инициализировать модульный логгер через `get_logger("<ENTITY>_ASSERTIONS")`.
- В каждой проверке писать `logger.info(...)` с понятным действием.

#### 5. Тесты

- Добавить тесты в `tests/<entity>/test_<entity>.py`.
- Покрыть CRUD и негативные кейсы (валидация, not found и т.д.).
- Парсить ответ в Pydantic-модель перед проверками.
- Делать валидацию JSON schema через `validate_json_schema`.
- Держать импорты только в начале файла.

### Правила Allure

#### На уровне класса

- `@allure.epic(...)`
- `@allure.feature(...)`
- `@allure.parent_suite(...)` должно совпадать с `epic`.
- `@allure.suite(...)` должно совпадать с `feature`.

#### На уровне теста

- `@allure.title(...)`
- `@allure.tag(...)`
- `@allure.story(...)`
- `@allure.sub_suite(...)` должно совпадать с `story`.
- `@allure.severity(...)`

#### На уровне шагов

- Методы клиентов и assertion-функции оформляются через `@allure.step(...)`.

### Логирование

- Использовать `get_logger` один раз на модуль.
- Логировать ключевые этапы проверок через `logger.info(...)`.

### Faker и тестовые данные

- Использовать `tools.fakers` для генерации валидных значений по умолчанию.
- Специальные значения задавать только для конкретного тестового сценария.

### Конфигурация

- Настройки хранить в `config.py` на базе `pydantic-settings`.
- Данные окружения читать из `.env`.
- Путь к файлам брать из `settings.test_data.*`, а не из строковых путей.

### Команды запуска

- Регресс: `python -m pytest -m "regression"`
- Регресс + Allure: `python -m pytest -m "regression" --alluredir=./allure-results`

## AI Guide: How to create new tests from Swagger/OpenAPI

This section describes the expected workflow for an AI assistant generating tests in this repository.

### Input expected from Swagger/OpenAPI

- Endpoint path and HTTP method.
- Request body schema and required fields.
- Query/path parameter schema.
- Success response schema(s).
- Error response schema(s) and status codes.
- Auth requirements (public/private).

### AI implementation algorithm

#### Step 1. Map endpoint to entity

- Decide target entity folder (`users`, `files`, `courses`, `exercises`, etc.).
- Reuse existing module layout; do not invent new architecture.

#### Step 2. Add or extend schemas

- Update/create schemas in `clients/<entity>/<entity>_schema.py`.
- Reflect OpenAPI contract exactly in types and aliases.
- Prefer strict models and explicit fields.

#### Step 3. Add client methods

- Update `clients/<entity>/<entity>_client.py`.
- Use `APIRoutes.<ENTITY>` instead of hardcoded routes.
- Add:
- low-level `<action>_api(...) -> Response`
- typed `<action>(...) -> <ResponseSchema>`
- Decorate public methods with `@allure.step`.

#### Step 4. Add fixtures if needed

- Update `fixtures/<entity>.py`.
- Create or extend fixture `BaseModel` aggregators.
- Add typed fixtures to build preconditions for tests.

#### Step 5. Add assertions

- Update `tools/assertions/<entity>.py`.
- Add field-by-field checks for all important fields.
- Reuse base assertion helpers and nested entity assertions.
- Add `@allure.step` and `logger.info(...)` to each function.

#### Step 6. Add tests

- Update or create `tests/<entity>/test_<entity>.py`.
- Include:
- positive status check
- payload assertions
- JSON schema validation
- Add negative tests for invalid data and not found where applicable.
- Add full Allure annotations on class and test levels.

#### Step 7. Replace hardcoded test data

- Never hardcode file paths or environment-specific values.
- Use `settings` from `config.py`.

#### Step 8. Validate changes

- Run targeted tests first (`python -m pytest -k "<test_name>"`).
- Run regression (`python -m pytest -m "regression"`).
- If changed Allure metadata, run with `--alluredir=./allure-results`.

### Mandatory quality gates for AI-generated code

- Imports are at module top only.
- Two blank lines after import block.
- No function-local imports unless truly required.
- Reusable logic goes to fixtures/assertions, not duplicated in tests.
- API contracts are validated via Pydantic and JSON schema.
- Allure hierarchy and steps are complete.
- Logging is present in assertions.
- New/changed tests pass.

## AI Contract (Swagger -> Tests)

This contract defines how an AI assistant must implement new API autotests in this repository.

### 1. Input contract (required)

AI must receive these fields for each method from Swagger/OpenAPI:

- HTTP method and endpoint path.
- Entity/tag name.
- Authentication type (public/private).
- Request schema: fields, required fields, constraints, defaults.
- Path/query/header parameters.
- Success response schema(s) and status code(s).
- Error response schema(s) and status code(s).
- Method description/business notes.

If any field is missing, AI must report `Missing input` first and list exactly what is required.

### 2. Execution contract (mandatory order)

AI must implement changes in this order:

1. Update/create Pydantic schemas in `clients/<entity>/<entity>_schema.py`.
2. Update/create client methods in `clients/<entity>/<entity>_client.py`.
3. Update/create fixtures in `fixtures/<entity>.py`.
4. Update/create assertions in `tools/assertions/<entity>.py`.
5. Update/create tests in `tests/<entity>/test_<entity>.py`.
6. Run targeted tests.
7. Run regression tests.

### 3. Repository standards (non-negotiable)

- Use `APIRoutes` enum; do not hardcode endpoint strings.
- Use `@allure.step(...)` for client action methods and assertion functions.
- Add full Allure hierarchy:
- class: `epic`, `feature`, `parent_suite`, `suite`
- test: `title`, `tag`, `story`, `sub_suite`, `severity`
- Parse API responses with Pydantic models.
- Validate response JSON schema in tests.
- Use reusable assertion helpers; avoid assertion duplication in tests.
- Initialize logger in assertion modules via `get_logger("<ENTITY>_ASSERTIONS")`.
- Add `logger.info(...)` to assertion functions.
- Keep imports only at top of file; no local imports unless truly required.
- Use settings/config values instead of hardcoded file paths or environment values.

### 4. Output contract (what AI must return)

AI final output must include:

1. Files changed.
2. What was implemented in each file.
3. Test commands executed.
4. Test results summary.
5. Assumptions made from Swagger descriptions.

### 5. Quality gates (must pass before completion)

AI must not finish until all checks are true:

- Schemas match Swagger/OpenAPI contract.
- Client methods use `APIRoutes` and have `allure.step`.
- Fixtures are typed and reusable.
- Assertions are extracted, logged, and reusable.
- Tests contain status checks, payload checks, schema validation, and Allure metadata.
- No hardcoded file paths for test data.
- Targeted tests pass.
- `python -m pytest -m "regression"` passes.

### 6. Reusable prompt template

Use this prompt when asking AI to generate tests from Swagger:

"Given Swagger/OpenAPI method description, implement tests according to README AI Contract and project rules. Update schemas, client, fixtures, assertions, and tests in repository structure. Use APIRoutes, Allure hierarchy, allure.step, logger.info, Pydantic parsing, JSON schema validation, and settings-based paths. Run targeted tests and regression, then report files changed and results."
