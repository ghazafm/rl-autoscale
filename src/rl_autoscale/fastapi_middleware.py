"""
FastAPI middleware for RL autoscaling metrics.

Provides automatic instrumentation for FastAPI applications.
"""

import logging
from typing import Callable, Optional

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .metrics import RLMetrics, get_metrics_registry, get_precise_time, start_metrics_server

logger = logging.getLogger(__name__)


class RLMetricsMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for RL autoscaling metrics.

    Automatically records request latency and count for all endpoints.
    """

    def __init__(
        self,
        app: FastAPI,
        metrics: RLMetrics,
        path_normalizer: Optional[Callable[[str], str]] = None,
        exclude_paths: Optional[list[str]] = None,
    ):
        super().__init__(app)
        self.metrics = metrics
        self.path_normalizer = path_normalizer
        self.exclude_paths = exclude_paths or [
            "/health",
            "/metrics",
            "/docs",
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next):
        """Process request and record metrics."""
        # Skip excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Track in-progress request
        self.metrics.inc_in_progress(request.method)

        # Record start time using high-precision timer
        start_time = get_precise_time()

        try:
            # Process request
            response: Response = await call_next(request)

            # Calculate duration
            duration = get_precise_time() - start_time

            # Get path (apply normalizer if provided)
            path = request.url.path
            if self.path_normalizer:
                try:
                    path = self.path_normalizer(path)
                except Exception as e:
                    logger.warning(f"Path normalizer failed for {path}: {e}")

            # Get response size from Content-Length header if available
            response_size = None
            content_length = response.headers.get("content-length")
            if content_length:
                try:
                    response_size = int(content_length)
                except ValueError:
                    pass

            # Record metrics
            try:
                self.metrics.observe_request(
                    method=request.method,
                    path=path,
                    duration=duration,
                    status_code=response.status_code,
                    response_size=response_size,
                )
            except Exception as e:
                logger.error(f"Failed to record metrics: {e}")

            return response
        finally:
            # Always decrement in-progress counter
            self.metrics.dec_in_progress(request.method)


def enable_metrics(
    app: FastAPI,
    port: Optional[int] = None,
    namespace: Optional[str] = None,
    histogram_buckets: Optional[list[float]] = None,
    response_size_buckets: Optional[list[float]] = None,
    path_normalizer: Optional[Callable[[str], str]] = None,
    exclude_paths: Optional[list[str]] = None,
    app_name: Optional[str] = None,
    app_version: Optional[str] = None,
) -> RLMetrics:
    """
    Enable RL autoscaling metrics for a FastAPI application.

    Usage:
        from fastapi import FastAPI
        from rl_autoscaling_observability import enable_metrics

        app = FastAPI()
        enable_metrics(app, port=8000)

        @app.get("/api/hello")
        async def hello():
            return {"message": "Hello World"}

    Environment variables:
        RL_METRICS_PORT: Default port for metrics server
        RL_METRICS_NAMESPACE: Default namespace prefix
        RL_METRICS_APP_NAME: Application name for info metric
        RL_METRICS_APP_VERSION: Application version for info metric

    Args:
        app: FastAPI application instance
        port: Port for Prometheus metrics server (env: RL_METRICS_PORT)
        namespace: Metric name prefix (env: RL_METRICS_NAMESPACE)
        histogram_buckets: Custom latency buckets
        response_size_buckets: Custom response size buckets
        path_normalizer: Function to normalize paths
        exclude_paths: Paths to exclude from metrics
        app_name: Application name (env: RL_METRICS_APP_NAME)
        app_version: Application version (env: RL_METRICS_APP_VERSION)

    Returns:
        RLMetrics instance
    """
    # Get or create metrics instance
    metrics = get_metrics_registry(
        namespace=namespace,
        histogram_buckets=histogram_buckets,
        response_size_buckets=response_size_buckets,
        app_name=app_name,
        app_version=app_version,
    )

    # Start metrics server
    try:
        start_metrics_server(port)
    except OSError:
        logger.warning(f"Metrics server on port {port} may already be running")

    # Add middleware
    app.add_middleware(
        RLMetricsMiddleware,
        metrics=metrics,
        path_normalizer=path_normalizer,
        exclude_paths=exclude_paths,
    )

    logger.info(f"✅ RL metrics enabled for FastAPI app (port={port}, namespace='{namespace}')")

    return metrics
