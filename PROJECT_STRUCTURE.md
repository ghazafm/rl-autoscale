# rl-autoscale Project Structure

This document explains the production-ready structure of the rl-autoscale package.

## Directory Structure

```
rl-autoscale/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Continuous Integration (tests, linting)
│       └── publish.yml         # Automated PyPI publishing
├── src/
│   └── rl_autoscale/           # Main package (underscore, not hyphen!)
│       ├── __init__.py         # Package entry point
│       ├── metrics.py          # Core metrics functionality
│       ├── flask_middleware.py # Flask integration
│       ├── fastapi_middleware.py # FastAPI integration
│       └── py.typed            # PEP 561 type checking marker
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_metrics.py
│   ├── test_flask_middleware.py
│   ├── test_fastapi_middleware.py
│   └── test_auto_detection.py
├── example_flask.py            # Example Flask app
├── example_fastapi.py          # Example FastAPI app
├── pyproject.toml              # Modern Python packaging config
├── setup.cfg                   # Pytest and coverage config
├── MANIFEST.in                 # Package file inclusion rules
├── README.md                   # User-facing documentation
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contributor guidelines
├── LICENSE                     # MIT License
├── SECURITY.md                 # Security policy
├── PUBLISHING.md               # PyPI publishing guide
├── build.sh                    # Quick build script
├── .gitignore                  # Git ignore rules
└── .dockerignore               # Docker ignore rules
```

## Key Design Decisions

### 1. src/ Layout (PEP 420)

**Why?**
- Prevents accidentally importing from source during development
- Forces installation before testing (catches packaging bugs early)
- Industry best practice for modern Python packages

**Structure:**
```
src/rl_autoscale/    # Module name uses underscore
```

### 2. Package vs Module Naming

- **PyPI Package Name**: `rl-autoscale` (hyphen allowed, user-friendly)
- **Python Module Name**: `rl_autoscale` (underscore required by Python)

Users install with: `pip install rl-autoscale`
But import with: `from rl_autoscale import ...`

### 3. Modern Packaging (PEP 517/518)

Using `pyproject.toml` instead of `setup.py`:
- ✅ Declarative configuration
- ✅ Build system independence
- ✅ Better dependency resolution
- ✅ Future-proof

### 4. Type Checking Support (PEP 561)

The `py.typed` marker file enables:
- Type checkers (mypy, pyright) can analyze your code
- IDEs provide better autocomplete
- Users get type hints when using the package

### 5. GitHub Actions CI/CD

**ci.yml** - Runs on every push/PR:
- Linting (ruff, black)
- Tests on Python 3.10, 3.11, 3.12
- Coverage reporting
- Package build verification

**publish.yml** - Runs on GitHub Release:
- Builds package
- Publishes to PyPI
- Uses trusted publishing (no tokens needed!)

## Configuration Files Explained

### pyproject.toml
**Purpose**: Main package configuration
**Contains**:
- Package metadata (name, version, description)
- Dependencies
- Optional dependencies (flask, fastapi, dev)
- Build system configuration
- Tool configurations (ruff)

### setup.cfg
**Purpose**: Test configuration
**Contains**:
- Pytest settings
- Coverage settings
- Test discovery rules

### MANIFEST.in
**Purpose**: Control which files are included in the package
**Important**: Only affects source distributions (`.tar.gz`)

### .gitignore
**Purpose**: Files Git should ignore
**Includes**:
- Python bytecode (`__pycache__`, `*.pyc`)
- Virtual environments
- Build artifacts
- IDE files

## Testing Strategy

### Unit Tests
Located in `tests/`:
- `test_metrics.py` - Core metrics functionality
- `test_flask_middleware.py` - Flask integration
- `test_fastapi_middleware.py` - FastAPI integration
- `test_auto_detection.py` - Framework detection

### Test Fixtures
`tests/conftest.py` provides:
- `flask_app` - Flask test application
- `fastapi_app` - FastAPI test application

### Running Tests

```bash
# Install with test dependencies
pip install -e ".[dev,flask,fastapi]"

# Run all tests
pytest

# Run with coverage
pytest --cov=rl_autoscale --cov-report=html

# Run specific test file
pytest tests/test_metrics.py

# Run specific test
pytest tests/test_metrics.py::test_metrics_singleton
```

## Publishing to PyPI

### Quick Method (Automated)

1. Update version in:
   - `pyproject.toml`
   - `src/rl_autoscale/__init__.py`
   - `CHANGELOG.md`

2. Create release on GitHub:
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
   Then create release on GitHub.com

3. GitHub Actions automatically publishes to PyPI

### Manual Method

```bash
# Run the build script
./build.sh

# Test on Test PyPI
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*
```

See `PUBLISHING.md` for detailed instructions.

## Development Workflow

### Initial Setup

```bash
# Clone repository
git clone https://github.com/ghazafm/rl-autoscale
cd rl-autoscale

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install in editable mode with all dependencies
pip install -e ".[dev,flask,fastapi]"
```

### Making Changes

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes to code

# 3. Format code
black .

# 4. Check linting
ruff check .

# 5. Run tests
pytest

# 6. Commit changes
git add .
git commit -m "Add my feature"

# 7. Push and create PR
git push origin feature/my-feature
```

### Pre-Commit Checklist

Before committing:
- [ ] Code formatted with `black .`
- [ ] Linting passes: `ruff check .`
- [ ] All tests pass: `pytest`
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

## Package Distribution

When you build the package (`python -m build`), it creates:

### 1. Source Distribution (`.tar.gz`)
```
dist/rl_autoscale-1.0.0.tar.gz
```
- Contains source code
- Users can build on any platform
- Includes files from MANIFEST.in

### 2. Wheel (`.whl`)
```
dist/rl_autoscale-1.0.0-py3-none-any.whl
```
- Pre-built binary distribution
- Faster to install
- Platform independent (pure Python)

## Common Tasks

### Add a New Dependency

Edit `pyproject.toml`:
```toml
dependencies = [
    "prometheus-client>=0.19.0",
    "your-new-dependency>=1.0.0",
]
```

### Add Optional Dependency

```toml
[project.optional-dependencies]
myfeature = [
    "some-package>=1.0.0",
]
```

Users install with: `pip install rl-autoscale[myfeature]`

### Update Version

1. `pyproject.toml`: Update `version = "1.0.1"`
2. `src/rl_autoscale/__init__.py`: Update `__version__ = "1.0.1"`
3. `CHANGELOG.md`: Add new version section

### Add New Module

1. Create file in `src/rl_autoscale/new_module.py`
2. Export in `src/rl_autoscale/__init__.py`:
   ```python
   from .new_module import MyClass
   __all__ = [..., "MyClass"]
   ```
3. Add tests in `tests/test_new_module.py`

## Troubleshooting

### "Module not found" during development

Install in editable mode:
```bash
pip install -e .
```

### Tests can't import package

Install with test dependencies:
```bash
pip install -e ".[dev]"
```

### Package build includes wrong files

Check `MANIFEST.in` and ensure proper patterns.

### Import error after PyPI install

Verify `[tool.setuptools.packages.find]` in `pyproject.toml`:
```toml
[tool.setuptools.packages.find]
where = ["src"]
include = ["rl_autoscale*"]
```

## Resources

- **Packaging Guide**: https://packaging.python.org/
- **PEP 517**: https://www.python.org/dev/peps/pep-0517/
- **PEP 518**: https://www.python.org/dev/peps/pep-0518/
- **PEP 561**: https://www.python.org/dev/peps/pep-0561/
- **Semantic Versioning**: https://semver.org/

## Questions?

- Check `CONTRIBUTING.md` for contribution guidelines
- Check `PUBLISHING.md` for publishing instructions
- Open an issue: https://github.com/ghazafm/rl-autoscale/issues
