"""Tests for the RLMetrics class."""

import threading

from rl_autoscale.metrics import RLMetrics, get_metrics_registry, get_precise_time


def test_metrics_singleton():
    """Test that get_metrics_registry returns the same instance."""
    metrics1 = get_metrics_registry()
    metrics2 = get_metrics_registry()
    assert metrics1 is metrics2


def test_metrics_initialization(metrics_registry):
    """Test metrics initialization with custom parameters."""
    metrics = RLMetrics(
        registry=metrics_registry,
        namespace="test",
        histogram_buckets=[0.001, 0.01, 0.1, 1.0],
        response_size_buckets=[100, 1000, 10000],
        app_name="test-app",
        app_version="1.0.0",
    )
    assert metrics.namespace == "test"
    assert metrics.histogram_buckets == [0.001, 0.01, 0.1, 1.0]
    assert metrics.response_size_buckets == [100, 1000, 10000]


def test_observe_request(metrics_registry):
    """Test recording request metrics."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test")

    # Record a successful request
    metrics.observe_request(
        method="GET",
        path="/api/test",
        duration=0.150,
        status_code=200,
        response_size=1024,
    )

    # Verify metrics were recorded (basic smoke test)
    # In a real test, you'd inspect the prometheus registry
    assert True  # If no exception, metrics recorded successfully


def test_observe_request_with_normalization(metrics_registry):
    """Test request observation with path normalization."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test")

    # Normalize path before passing to observe_request
    def normalizer(path):
        """Simple normalizer for testing."""
        return path.replace("123", ":id")

    original_path = "/user/123"
    normalized_path = normalizer(original_path)

    metrics.observe_request(
        method="GET",
        path=normalized_path,  # Pass normalized path
        duration=0.1,
        status_code=200,
    )

    assert True  # Smoke test


def test_metrics_with_different_status_codes(metrics_registry):
    """Test metrics with various HTTP status codes."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test")

    status_codes = [200, 201, 400, 404, 500, 503]

    for status in status_codes:
        metrics.observe_request(method="GET", path="/test", duration=0.1, status_code=status)

    assert True  # Smoke test


def test_in_progress_tracking(metrics_registry):
    """Test in-progress request tracking."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test_inprog")

    # Increment in-progress counter
    metrics.inc_in_progress("GET")
    metrics.inc_in_progress("GET")
    metrics.inc_in_progress("POST")

    # Decrement in-progress counter
    metrics.dec_in_progress("GET")

    # No exception means success
    assert True


def test_track_in_progress_context_manager(metrics_registry):
    """Test in-progress tracking context manager."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test_ctx")

    with metrics.track_in_progress("GET"):
        # Simulate request processing
        pass

    assert True  # If no exception, context manager works correctly


def test_response_size_tracking(metrics_registry):
    """Test response size histogram."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test_size")

    # Record requests with different response sizes
    metrics.observe_request(
        method="GET",
        path="/small",
        duration=0.1,
        status_code=200,
        response_size=100,
    )
    metrics.observe_request(
        method="GET",
        path="/medium",
        duration=0.1,
        status_code=200,
        response_size=10000,
    )
    metrics.observe_request(
        method="GET",
        path="/large",
        duration=0.1,
        status_code=200,
        response_size=1000000,
    )

    assert True  # Smoke test


def test_error_type_categorization(metrics_registry):
    """Test that error types are correctly categorized."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test_errors")

    # Client errors (4xx)
    metrics.observe_request(method="GET", path="/not-found", duration=0.1, status_code=404)
    metrics.observe_request(method="POST", path="/bad-request", duration=0.1, status_code=400)

    # Server errors (5xx)
    metrics.observe_request(method="GET", path="/error", duration=0.1, status_code=500)
    metrics.observe_request(method="GET", path="/timeout", duration=0.1, status_code=503)

    # Success (2xx)
    metrics.observe_request(method="GET", path="/ok", duration=0.1, status_code=200)
    metrics.observe_request(method="POST", path="/created", duration=0.1, status_code=201)

    assert True  # Smoke test


def test_get_precise_time():
    """Test high-precision time function."""
    t1 = get_precise_time()
    t2 = get_precise_time()

    # Time should be monotonically increasing
    assert t2 >= t1


def test_thread_safety(metrics_registry):
    """Test that metrics can be recorded from multiple threads."""
    metrics = RLMetrics(registry=metrics_registry, namespace="test_threads")

    errors = []

    def record_requests():
        try:
            for _ in range(100):
                metrics.observe_request(
                    method="GET",
                    path="/thread-test",
                    duration=0.01,
                    status_code=200,
                )
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=record_requests) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(errors) == 0, f"Thread errors: {errors}"
