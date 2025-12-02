"""
Core metrics definitions for RL autoscaling.

This module provides standardized Prometheus metrics that are expected by
RL-based autoscaling agents.
"""

import logging
import os
import threading
import time
from typing import Optional

from prometheus_client import Counter, Gauge, Histogram, Info, start_http_server
from prometheus_client.registry import REGISTRY, CollectorRegistry

logger = logging.getLogger(__name__)

# Thread-safe singleton lock
_metrics_lock = threading.Lock()


class RLMetrics:
    """
    Standardized metrics for RL autoscaling systems.

    This class encapsulates all metrics required by RL autoscaling agents:
    - Request latency (histogram for percentile calculation)
    - Request count (for throughput analysis)

    The metrics follow Prometheus naming conventions and are designed to be
    scraped at regular intervals (typically 15-60 seconds).
    """

    def __init__(
        self,
        registry: Optional[CollectorRegistry] = None,
        namespace: str = "",
        histogram_buckets: Optional[list[float]] = None,
        response_size_buckets: Optional[list[float]] = None,
        app_version: str = "",
        app_name: str = "",
    ):
        """
        Initialize metrics collectors.

        Args:
            registry: Prometheus registry (default: global REGISTRY)
            namespace: Metric name prefix (e.g., "myapp" -> "myapp_http_...")
            histogram_buckets: Custom histogram buckets for latency
                              Default optimized for web APIs: 5ms to 10s
            response_size_buckets: Custom histogram buckets for response size
                                  Default: 100B to 10MB
            app_version: Application version for info metric
            app_name: Application name for info metric
        """
        self.registry = registry or REGISTRY
        self.namespace = namespace

        # Default buckets cover 5ms to 10s (optimized for web APIs)
        if histogram_buckets is None:
            histogram_buckets = [
                0.005,  # 5ms
                0.01,  # 10ms
                0.025,  # 25ms
                0.05,  # 50ms
                0.1,  # 100ms
                0.25,  # 250ms
                0.5,  # 500ms
                1.0,  # 1s
                2.5,  # 2.5s
                5.0,  # 5s
                10.0,  # 10s
            ]

        self.histogram_buckets = histogram_buckets

        # Default response size buckets: 100B to 10MB
        if response_size_buckets is None:
            response_size_buckets = [
                100,  # 100B
                1_000,  # 1KB
                10_000,  # 10KB
                100_000,  # 100KB
                1_000_000,  # 1MB
                10_000_000,  # 10MB
            ]

        self.response_size_buckets = response_size_buckets

        # Request latency histogram
        # Used by RL agent to calculate response time percentiles
        self.request_latency = Histogram(
            name=f"{namespace}_http_request_duration_seconds"
            if namespace
            else "http_request_duration_seconds",
            documentation="HTTP request latency in seconds",
            labelnames=["method", "path"],
            buckets=self.histogram_buckets,
            registry=self.registry,
        )

        # Request counter
        # Used by RL agent to understand traffic patterns
        self.request_count = Counter(
            name=f"{namespace}_http_requests_total" if namespace else "http_requests_total",
            documentation="Total HTTP requests",
            labelnames=["method", "path", "http_status", "error_type"],
            registry=self.registry,
        )

        # In-progress requests gauge (CRITICAL for saturation detection)
        # Used by RL agent to understand current load/saturation
        self.requests_in_progress = Gauge(
            name=f"{namespace}_http_requests_in_progress"
            if namespace
            else "http_requests_in_progress",
            documentation="Number of HTTP requests currently being processed",
            labelnames=["method"],
            registry=self.registry,
        )

        # Response size histogram
        # Used by RL agent for bandwidth analysis
        self.response_size = Histogram(
            name=f"{namespace}_http_response_size_bytes"
            if namespace
            else "http_response_size_bytes",
            documentation="HTTP response size in bytes",
            labelnames=["method", "path"],
            buckets=self.response_size_buckets,
            registry=self.registry,
        )

        # Application info metric
        # Useful for identifying pods/versions in Kubernetes
        self.app_info = Info(
            name=f"{namespace}_app" if namespace else "app",
            documentation="Application information",
            registry=self.registry,
        )

        # Set app info if provided
        info_labels = {}
        if app_name:
            info_labels["name"] = app_name
        if app_version:
            info_labels["version"] = app_version
        if info_labels:
            self.app_info.info(info_labels)

        # Application start timestamp
        # Useful for RL agents to understand pod lifecycle
        self.app_started_timestamp = Gauge(
            name=f"{namespace}_app_started_timestamp_seconds"
            if namespace
            else "app_started_timestamp_seconds",
            documentation="Unix timestamp when application started",
            registry=self.registry,
        )
        self.app_started_timestamp.set_to_current_time()

        logger.info(
            f"Initialized RL metrics with namespace='{namespace}', "
            f"buckets={len(self.histogram_buckets)}"
        )

    def observe_request(
        self,
        method: str,
        path: str,
        duration: float,
        status_code: int,
        response_size: Optional[int] = None,
    ) -> None:
        """
        Record a single HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: Request path (e.g., "/api/users")
            duration: Request duration in seconds
            status_code: HTTP status code (200, 404, etc.)
            response_size: Response body size in bytes (optional)
        """
        try:
            # Determine error type for better categorization
            error_type = "none"
            if 400 <= status_code < 500:
                error_type = "client_error"
            elif status_code >= 500:
                error_type = "server_error"

            self.request_latency.labels(method=method, path=path).observe(duration)
            self.request_count.labels(
                method=method, path=path, http_status=str(status_code), error_type=error_type
            ).inc()

            # Record response size if provided
            if response_size is not None:
                self.response_size.labels(method=method, path=path).observe(response_size)
        except Exception as e:
            logger.error(f"Failed to record metrics: {e}", exc_info=True)

    def track_in_progress(self, method: str):
        """
        Context manager to track in-progress requests.

        Usage:
            with metrics.track_in_progress("GET"):
                # handle request
                pass

        Args:
            method: HTTP method (GET, POST, etc.)

        Returns:
            Context manager that increments/decrements the in-progress gauge
        """
        return self.requests_in_progress.labels(method=method).track_inprogress()

    def inc_in_progress(self, method: str) -> None:
        """Increment the in-progress counter for a method."""
        self.requests_in_progress.labels(method=method).inc()

    def dec_in_progress(self, method: str) -> None:
        """Decrement the in-progress counter for a method."""
        self.requests_in_progress.labels(method=method).dec()


# Global metrics registry instance
_metrics_instance: Optional[RLMetrics] = None


def get_metrics_registry(
    namespace: Optional[str] = None,
    histogram_buckets: Optional[list[float]] = None,
    response_size_buckets: Optional[list[float]] = None,
    app_version: Optional[str] = None,
    app_name: Optional[str] = None,
) -> RLMetrics:
    """
    Get or create the global metrics instance (thread-safe).

    Environment variables:
        RL_METRICS_NAMESPACE: Default namespace prefix
        RL_METRICS_APP_NAME: Application name for info metric
        RL_METRICS_APP_VERSION: Application version for info metric

    Args:
        namespace: Metric name prefix (env: RL_METRICS_NAMESPACE)
        histogram_buckets: Custom histogram buckets
        response_size_buckets: Custom response size buckets
        app_version: Application version (env: RL_METRICS_APP_VERSION)
        app_name: Application name (env: RL_METRICS_APP_NAME)

    Returns:
        Global RLMetrics instance
    """
    global _metrics_instance

    if _metrics_instance is None:
        with _metrics_lock:
            # Double-check locking pattern for thread safety
            if _metrics_instance is None:
                # Apply environment variable defaults
                if namespace is None:
                    namespace = os.getenv("RL_METRICS_NAMESPACE", "")
                if app_name is None:
                    app_name = os.getenv("RL_METRICS_APP_NAME", "")
                if app_version is None:
                    app_version = os.getenv("RL_METRICS_APP_VERSION", "")

                _metrics_instance = RLMetrics(
                    namespace=namespace,
                    histogram_buckets=histogram_buckets,
                    response_size_buckets=response_size_buckets,
                    app_version=app_version,
                    app_name=app_name,
                )

    return _metrics_instance


def start_metrics_server(port: Optional[int] = None) -> None:
    """
    Start Prometheus metrics HTTP server.

    This starts a simple HTTP server that exposes metrics at /metrics endpoint.
    Prometheus scrapes this endpoint at regular intervals.

    Environment variables:
        RL_METRICS_PORT: Default port for metrics server

    Args:
        port: Port number for metrics server (default: 8000, env: RL_METRICS_PORT)

    Raises:
        OSError: If port is already in use
    """
    if port is None:
        port = int(os.getenv("RL_METRICS_PORT", "8000"))

    try:
        start_http_server(port)
        logger.info(f"✅ Metrics server started on port {port}")
        logger.info(f"📊 Metrics available at http://localhost:{port}/metrics")
    except OSError as e:
        if "Address already in use" in str(e):
            logger.warning(f"⚠️  Port {port} already in use, metrics server may already be running")
        else:
            logger.error(f"Failed to start metrics server on port {port}: {e}")
            raise


def get_precise_time() -> float:
    """
    Get high-precision time for request duration measurement.

    Uses time.perf_counter() for better precision than time.time().

    Returns:
        Current time in seconds (high precision)
    """
    return time.perf_counter()
