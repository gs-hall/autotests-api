from typing import Any, Callable

from swagger_coverage_tool import SwaggerCoverageTracker

from tools.logger import get_logger

logger = get_logger("API_COVERAGE")


class _NoopSwaggerCoverageTracker:
    def track_coverage_httpx(self, _path: str) -> Callable[[Any], Any]:
        def decorator(func: Any) -> Any:
            return func

        return decorator


try:
    # 'api-course' must match the key in SWAGGER_COVERAGE_SERVICES.
    tracker: SwaggerCoverageTracker | _NoopSwaggerCoverageTracker = (
        SwaggerCoverageTracker(service="api-course")
    )
except Exception as exc:
    logger.warning("Swagger coverage disabled due to settings error: %s", exc)
    tracker = _NoopSwaggerCoverageTracker()
