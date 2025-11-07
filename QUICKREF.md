# Quick Reference: UV + Ruff Commands

Fast reference for development with UV and Ruff.

## 🚀 Setup (First Time)

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project (ONE COMMAND!)
git clone https://github.com/ghazafm/rl-autoscale
cd rl-autoscale
uv sync --all-extras

# That's it! You're ready to develop.
# UV automatically creates venv and installs everything.
```

## 📦 Package Management

```bash
# Sync project (recreate env if needed)
uv sync --all-extras

# Sync with specific extras only
uv sync --extra dev --extra flask

# Add new dependency (updates pyproject.toml)
uv add package-name

# Add dev dependency
uv add --dev package-name

# Remove dependency
uv remove package-name

# Update dependencies
uv sync --upgrade

# List installed
uv pip list
```

## 🎨 Code Quality

```bash
# Format code
ruff format .

# Check formatting (no changes)
ruff format --check .

# Lint code
ruff check .

# Auto-fix linting
ruff check . --fix

# Format + Lint (recommended workflow)
ruff format . && ruff check .
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=rl_autoscale

# Specific test file
uv run pytest tests/test_metrics.py

# Verbose output
uv run pytest -v

# Coverage report (HTML)
uv run pytest --cov=rl_autoscale --cov-report=html
open htmlcov/index.html
```

## 🏗️ Building

```bash
# Clean build
rm -rf dist/ build/ src/*.egg-info

# Build package
uv run python -m build

# Check package
twine check dist/*

# Or use the script
./build.sh
```

## 🚀 Running

```bash
# Run Python script
uv run python example_flask.py

# Run with specific Python version
uv run --python 3.12 python script.py

# Run command in venv
uv run <command>
```

## 🔍 Verification

```bash
# Check everything
./verify.sh

# Or manually:
ruff format --check .    # Check formatting
ruff check .             # Check linting
uv run pytest            # Run tests
uv run python -m build   # Build package
```

## 📝 Git Workflow

```bash
# Before commit
ruff format .
ruff check . --fix
uv run pytest

# Commit
git add .
git commit -m "Your message"
git push
```

## 🎯 Common Tasks

| Task | Command |
|------|---------|
| Format all files | `ruff format .` |
| Check formatting | `ruff format --check .` |
| Lint code | `ruff check .` |
| Fix linting | `ruff check . --fix` |
| Run tests | `uv run pytest` |
| Test with coverage | `uv run pytest --cov=rl_autoscale` |
| Build package | `uv run python -m build` |
| Install deps | `uv pip install -e ".[dev]"` |
| Run example | `uv run python example_flask.py` |

## ⚡ Why UV + Ruff?

- **UV**: 10-100x faster than pip
- **Ruff**: 10-100x faster than black + pylint
- **Simpler**: One tool for formatting + linting
- **Modern**: Latest Python tooling standards

## 🔗 Full Guides

- **UV Guide**: [UV_GUIDE.md](UV_GUIDE.md)
- **Project Structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Publishing**: [PUBLISHING.md](PUBLISHING.md)

---

**Pro Tip**: Add these to your shell aliases!

```bash
# ~/.zshrc or ~/.bashrc
alias uvt="uv run pytest"
alias uvtc="uv run pytest --cov=rl_autoscale"
alias fmt="ruff format . && ruff check ."
alias check="ruff format --check . && ruff check ."
```
