"""
Example: Flask application with RL autoscaling metrics

This example shows how simple it is to add metrics to your Flask app.
Before: 50+ lines of prometheus_client boilerplate
After: 2 lines with rl_autoscaling_observability
"""

from flask import Flask, jsonify

from rl_autoscaler_exporter import enable_metrics

# Create Flask app
app = Flask(__name__)

# 🎯 Enable metrics (that's it!)
enable_metrics(app, port=8000)


# Define your routes normally
@app.route("/")
def index():
    return "Welcome to Flask with RL Metrics!"


@app.route("/api/users")
def get_users():
    # Simulate some work
    import time

    time.sleep(0.1)

    return jsonify(
        {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
            ]
        }
    )


@app.route("/api/slow")
def slow_endpoint():
    # Simulate slow operation
    import time

    time.sleep(2.0)
    return jsonify({"status": "completed"})


@app.route("/health")
def health():
    # Health check endpoints are automatically excluded from metrics
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    print("🚀 Flask app with RL metrics running!")
    print("📊 Metrics: http://localhost:8000/metrics")
    print("🌐 App: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
