# Contributing to rl-autoscale

Thank you for your interest in contributing! 🎉

## Development Setup

```bash
# Clone the repository
git clone https://github.com/ghazafm/rl-autoscale.git
cd rl-autoscale

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev,flask,fastapi]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=rl_autoscale --cov-report=html

# Run specific test
pytest tests/test_flask_middleware.py
```

## Code Style

We use `black` for formatting and `ruff` for linting:

```bash
# Format code
black .

# Lint code
ruff check .

# Fix linting issues automatically
ruff check --fix .
```

## Submitting Changes

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/my-feature`
3. **Make changes** and add tests
4. **Run tests**: `pytest`
5. **Format code**: `black .`
6. **Commit**: `git commit -m "Add my feature"`
7. **Push**: `git push origin feature/my-feature`
8. **Create Pull Request**

## Pull Request Guidelines

- ✅ Add tests for new features
- ✅ Update documentation (README.md)
- ✅ Follow existing code style
- ✅ Keep PRs focused (one feature/fix per PR)
- ✅ Write clear commit messages

## Adding Support for New Frameworks

To add support for a new framework (e.g., Django):

1. Create `django_middleware.py`:
   ```python
   from .metrics import get_metrics_registry

   def enable_metrics(app, port=8000, **kwargs):
       # Framework-specific implementation
       pass
   ```

2. Update `__init__.py` to detect the framework

3. Add tests in `tests/test_django_middleware.py`

4. Update README.md with usage example

## Questions?

Open an issue or discussion on GitHub!
