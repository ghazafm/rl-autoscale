"""
RL Autoscale - Production-Ready Metrics for RL-Based Autoscaling

A lightweight Python library for instrumenting applications with standardized
metrics for reinforcement learning-based autoscaling systems.

Usage:
    from rl_autoscale import enable_metrics

    app = Flask(__name__)
    enable_metrics(app, port=8000)
"""

from typing import Optional

from .metrics import RLMetrics, get_metrics_registry, get_precise_time

__version__ = "1.0.4"
__all__ = [
    "RLMetrics",
    "enable_metrics",
    "enable_flask_metrics",
    "enable_fastapi_metrics",
    "get_metrics_registry",
    "get_precise_time",
]


def enable_flask_metrics(app, port: Optional[int] = None, **kwargs):
    """
    Enable metrics for Flask applications.

    This function is lazily imported to avoid requiring Flask as a dependency
    when it's not needed.

    Environment variables:
        RL_METRICS_PORT: Default port for metrics server
        RL_METRICS_NAMESPACE: Default namespace prefix
        RL_METRICS_APP_NAME: Application name for info metric
        RL_METRICS_APP_VERSION: Application version for info metric
    """
    from .flask_middleware import enable_metrics as _enable_flask_metrics

    return _enable_flask_metrics(app, port=port, **kwargs)


def enable_fastapi_metrics(app, port: Optional[int] = None, **kwargs):
    """
    Enable metrics for FastAPI applications.

    This function is lazily imported to avoid requiring FastAPI as a dependency
    when it's not needed.

    Environment variables:
        RL_METRICS_PORT: Default port for metrics server
        RL_METRICS_NAMESPACE: Default namespace prefix
        RL_METRICS_APP_NAME: Application name for info metric
        RL_METRICS_APP_VERSION: Application version for info metric
    """
    from .fastapi_middleware import enable_metrics as _enable_fastapi_metrics

    return _enable_fastapi_metrics(app, port=port, **kwargs)


def enable_metrics(app, port: Optional[int] = None, **kwargs):
    """
    Auto-detect framework and enable metrics.

    Args:
        app: Flask, FastAPI, or other WSGI/ASGI application
        port: Port for Prometheus metrics endpoint (env: RL_METRICS_PORT)
        **kwargs: Additional configuration options

    Environment variables:
        RL_METRICS_PORT: Default port for metrics server (default: 8000)
        RL_METRICS_NAMESPACE: Default namespace prefix
        RL_METRICS_APP_NAME: Application name for info metric
        RL_METRICS_APP_VERSION: Application version for info metric

    Returns:
        Configured metrics instance
    """
    # Detect Flask
    if hasattr(app, "before_request") and hasattr(app, "after_request"):
        return enable_flask_metrics(app, port=port, **kwargs)

    # Detect FastAPI
    if hasattr(app, "add_middleware"):
        return enable_fastapi_metrics(app, port=port, **kwargs)

    raise ValueError(f"Unsupported framework: {type(app).__name__}. Supported: Flask, FastAPI")
