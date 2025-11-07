"""Pytest configuration and fixtures."""

import pytest
from prometheus_client import CollectorRegistry


@pytest.fixture
def metrics_registry():
    """Create a fresh Prometheus registry for each test."""
    return CollectorRegistry()


@pytest.fixture
def flask_app():
    """Create a Flask test application."""
    try:
        from flask import Flask

        app = Flask(__name__)

        @app.route("/test")
        def test_route():
            return "OK"

        return app
    except ImportError:
        pytest.skip("Flask not installed")


@pytest.fixture
def fastapi_app():
    """Create a FastAPI test application."""
    try:
        from fastapi import FastAPI

        app = FastAPI()

        @app.get("/test")
        async def test_route():
            return {"status": "OK"}

        return app
    except ImportError:
        pytest.skip("FastAPI not installed")
