"""
Example: FastAPI application with RL autoscaling metrics

Shows how to use rl_autoscaling_observability with FastAPI.
"""

from fastapi import FastAPI

from rl_autoscaler_exporter import enable_metrics

# Create FastAPI app
app = FastAPI(title="FastAPI with RL Metrics")

# 🎯 Enable metrics (that's it!)
enable_metrics(app, port=8000)


# Define your routes normally
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with RL Metrics!"}


@app.get("/api/users")
async def get_users():
    # Simulate async work
    import asyncio

    await asyncio.sleep(0.1)

    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
    }


@app.get("/api/slow")
async def slow_endpoint():
    # Simulate slow async operation
    import asyncio

    await asyncio.sleep(2.0)
    return {"status": "completed"}


@app.get("/health")
async def health():
    # Health checks automatically excluded from metrics
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    print("🚀 FastAPI app with RL metrics running!")
    print("📊 Metrics: http://localhost:8000/metrics")
    print("🌐 App: http://localhost:5000")
    print("📖 Docs: http://localhost:5000/docs")
    uvicorn.run(app, host="0.0.0.0", port=5000)
