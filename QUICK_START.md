# 🚀 Quick Start Guide

The fastest way to get started with rl-autoscale development.

---

## ⚡ Super Quick Start (3 Commands)

```bash
# 1. Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone project
git clone https://github.com/ghazafm/rl-autoscale
cd rl-autoscale

# 3. Setup everything!
uv sync --all-extras

# ✅ Done! You're ready to develop.
```

---

## 🎯 What Just Happened?

`uv sync --all-extras` automatically:
- ✅ Created `.venv` directory
- ✅ Installed package in editable mode
- ✅ Installed ALL dependencies (dev, flask, fastapi)
- ✅ Created `uv.lock` lockfile for reproducibility
- ✅ You're ready to code!

**Time**: ~10-15 seconds (vs ~2-3 minutes with pip)

---

## 🧪 Verify Installation

```bash
# Check it's installed
uv pip list | grep rl-autoscale
# Output: rl-autoscale    1.0.0    editable

# Run tests
uv run pytest
# Output: ===== 10 passed in 2.5s =====

# Format code
ruff format .
# Output: 5 files already formatted

# You're good to go! 🎉
```

---

## 💻 Daily Development Workflow

```bash
# 1. Edit code
vim src/rl_autoscale/metrics.py

# 2. Format & lint
ruff format . && ruff check .

# 3. Run tests
uv run pytest

# 4. Commit
git add . && git commit -m "Your changes"
```

**That's it!** Simple and fast. ⚡

---

## 📦 Common Tasks

### Add New Dependency
```bash
# Add runtime dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# This automatically updates pyproject.toml!
```

### Update Dependencies
```bash
# Update all dependencies
uv sync --upgrade

# Resync if pyproject.toml changed
uv sync
```

### Run Commands
```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=rl_autoscale

# Run examples
uv run python example_flask.py

# Build package
uv run python -m build
```

---

## 🎨 Code Quality

```bash
# Format code (100x faster than black!)
ruff format .

# Check linting
ruff check .

# Auto-fix linting issues
ruff check . --fix

# One-liner: format + lint + test
ruff format . && ruff check . && uv run pytest
```

---

## 🏗️ Build & Publish

```bash
# Build package (automated script)
./build.sh

# Or manually
rm -rf dist/ && uv run python -m build

# Upload to PyPI
twine upload dist/*
```

---

## 🔄 Update Your Environment

```bash
# If pyproject.toml changed
uv sync

# If you want to recreate everything
rm -rf .venv uv.lock
uv sync --all-extras
```

---

## 💡 Pro Tips

### 1. No Need to Activate venv
```bash
# UV commands work without activation
uv run pytest        # ✅ Works!
uv run python app.py # ✅ Works!

# But you can still activate if you want
source .venv/bin/activate
pytest               # ✅ Also works!
```

### 2. Use `uv sync` Over `uv pip install`
```bash
# Old way (manual)
uv venv
uv pip install -e ".[dev]"

# New way (automatic) ⭐
uv sync --all-extras
```

### 3. Lockfile for Reproducibility
```bash
# uv.lock ensures everyone has same versions
# Commit it to git!
git add uv.lock
```

### 4. Fast Dependency Management
```bash
# Add package: Updates pyproject.toml automatically
uv add requests

# Remove package: Updates pyproject.toml automatically
uv remove requests
```

---

## 🆚 UV Sync vs UV Pip

| Feature | `uv sync` | `uv pip install` |
|---------|-----------|------------------|
| Creates venv | ✅ Auto | ❌ Manual (`uv venv`) |
| Installs package | ✅ Auto | ✅ Manual |
| Creates lockfile | ✅ Yes | ❌ No |
| Updates deps | ✅ `--upgrade` | ⚠️ Manual |
| Add deps | ✅ `uv add` | ⚠️ Manual edit |
| **Recommended** | ✅ **Yes** | ⚠️ Legacy |

**TL;DR**: Use `uv sync` for everything! It's modern and automatic.

---

## 📚 Need More Details?

- **Complete Guide**: [STEP_BY_STEP.md](STEP_BY_STEP.md) - Every detail explained
- **Checklist**: [CHECKLIST.md](CHECKLIST.md) - Track your progress
- **UV Deep Dive**: [UV_GUIDE.md](UV_GUIDE.md) - Master UV
- **Quick Reference**: [QUICKREF.md](QUICKREF.md) - All commands
- **Visual Guide**: [WORKFLOW.md](WORKFLOW.md) - See the process

---

## 🎯 Summary

**Modern Workflow with UV:**
```bash
git clone <repo>           # Clone
uv sync --all-extras       # Setup (automatic!)
ruff format .              # Format
ruff check .               # Lint
uv run pytest              # Test
./build.sh                 # Build
twine upload dist/*        # Publish
```

**That's it!** Fast, simple, and modern. 🚀

---

## 🆘 Troubleshooting

### UV not found
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

### Sync fails
```bash
rm -rf .venv uv.lock
uv sync --all-extras
```

### Import errors
```bash
# Ensure you're in project directory
cd /path/to/rl-autoscale
uv sync
```

### Old venv conflicts
```bash
rm -rf venv .venv
uv sync --all-extras
```

---

## ✅ You're Ready!

You now know:
- ✅ `uv sync --all-extras` - One command setup
- ✅ `uv run` - Run commands without activating
- ✅ `uv add` - Add dependencies automatically
- ✅ `ruff format` + `ruff check` - Fast code quality
- ✅ Modern Python development workflow

**Start coding!** 🎉

---

**Next Steps:**
1. Try it: `uv sync --all-extras`
2. Run tests: `uv run pytest`
3. Read: [STEP_BY_STEP.md](STEP_BY_STEP.md) for publishing guide
