# 🚀 Complete Step-by-Step Guide: Setup to PyPI

This guide walks you through **every step** from initial setup to publishing on PyPI.

---

## 📋 Table of Contents

1. [Initial Setup](#1-initial-setup)
2. [Development Workflow](#2-development-workflow)
3. [Testing](#3-testing)
4. [Code Quality](#4-code-quality)
5. [Building the Package](#5-building-the-package)
6. [Testing the Build](#6-testing-the-build)
7. [Publishing to Test PyPI](#7-publishing-to-test-pypi)
8. [Publishing to PyPI](#8-publishing-to-pypi)
9. [Post-Publishing](#9-post-publishing)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Initial Setup

### Step 1.1: Install UV Package Manager

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation:**
```bash
uv --version
# Should show: uv 0.x.x
```

**Restart your terminal** to ensure UV is in your PATH.

---

### Step 1.2: Clone the Repository (if not already)

```bash
cd ~/Documents/code  # or wherever you want
git clone https://github.com/ghazafm/rl-autoscale
cd rl-autoscale
```

**Pro Tip**: With UV, you can also do this in one command:
```bash
uv init --lib rl-autoscale  # For new projects
# But since you already have the project, just clone it
```

---

### Step 1.3: Setup Environment and Install Everything (One Command!)

```bash
# UV sync does everything: creates venv + installs all dependencies
uv sync --all-extras

# This single command:
# 1. Creates .venv directory automatically
# 2. Installs the package in editable mode
# 3. Installs ALL extras (dev, flask, fastapi)
# 4. Creates a lockfile (uv.lock) for reproducibility

# Output should show:
# Using Python 3.11 interpreter at: /usr/bin/python3
# Creating virtualenv at: .venv
# Resolved X packages in XXXms
# Installed X packages in XXXms
```

**Alternative: Install specific extras only**
```bash
# Only dev tools
uv sync --extra dev

# Dev + Flask
uv sync --extra dev --extra flask

# Dev + FastAPI
uv sync --extra dev --extra fastapi
```

**Verify installation:**
```bash
uv pip list | grep rl-autoscale
# Should show: rl-autoscale 1.0.0 (editable)
```

**Why `uv sync` is better:**
- ✅ **One command** instead of two (venv + install)
- ✅ **Creates lockfile** (`uv.lock`) for reproducible builds
- ✅ **Faster** - UV's parallel installation
- ✅ **Automatic** - No need to activate venv

---

### Step 1.5: Verify Project Structure

```bash
# Run verification script
./verify.sh

# Should show all green checkmarks ✓
```

---

## 2. Development Workflow

### Step 2.1: Make Code Changes

Edit files in `src/rl_autoscale/`:
```bash
# Open in VS Code
code src/rl_autoscale/

# Or use any editor
vim src/rl_autoscale/metrics.py
```

---

### Step 2.2: Format Code

```bash
# Format all Python files
ruff format .

# Output:
# 5 files reformatted
```

---

### Step 2.3: Check Linting

```bash
# Check for issues
ruff check .

# Auto-fix fixable issues
ruff check . --fix

# Should show: All checks passed!
```

---

### Step 2.4: Run Examples (Optional)

```bash
# Test Flask example
uv run python example_flask.py
# Visit: http://localhost:5000/test

# Test FastAPI example (in another terminal)
uv run python example_fastapi.py
# Visit: http://localhost:8000/test
```

---

## 3. Testing

### Step 3.1: Run All Tests

```bash
# Run complete test suite
uv run pytest

# Output should show:
# ===== test session starts =====
# collected 10 items
#
# tests/test_metrics.py ......     [60%]
# tests/test_flask_middleware.py ..     [80%]
# tests/test_fastapi_middleware.py ..   [90%]
# tests/test_auto_detection.py .        [100%]
#
# ===== 10 passed in 2.5s =====
```

---

### Step 3.2: Run Tests with Coverage

```bash
# Generate coverage report
uv run pytest --cov=rl_autoscale --cov-report=html --cov-report=term

# Output shows coverage percentage
# Coverage HTML report generated in htmlcov/
```

---

### Step 3.3: View Coverage Report

```bash
# Open HTML coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

**Goal**: Aim for >80% code coverage.

---

### Step 3.4: Run Specific Tests

```bash
# Run specific test file
uv run pytest tests/test_metrics.py

# Run specific test function
uv run pytest tests/test_metrics.py::test_metrics_singleton

# Run with verbose output
uv run pytest -v

# Run and stop at first failure
uv run pytest -x
```

---

## 4. Code Quality

### Step 4.1: Format Check (CI-style)

```bash
# Check if code is properly formatted (doesn't modify files)
ruff format --check .

# If any files need formatting, you'll see:
# Would reformat: src/rl_autoscale/metrics.py
# 1 file would be reformatted

# Then run:
ruff format .
```

---

### Step 4.2: Lint Check (CI-style)

```bash
# Check for linting issues
ruff check .

# Common issues and fixes:
# - Unused imports: ruff check . --fix
# - Line too long: Format with ruff format .
# - Import sorting: ruff check . --fix
```

---

### Step 4.3: Full Quality Check

```bash
# Run everything at once
ruff format . && ruff check . && uv run pytest

# This is what CI does!
# All three must pass before committing.
```

---

## 5. Building the Package

### Step 5.1: Update Version (Before Building)

**Only if releasing a new version!**

Edit three files:

**File 1: `pyproject.toml`**
```toml
[project]
version = "1.0.1"  # Update this
```

**File 2: `src/rl_autoscale/__init__.py`**
```python
__version__ = "1.0.1"  # Update this
```

**File 3: `CHANGELOG.md`**
```markdown
## [1.0.1] - 2025-11-07

### Fixed
- Bug fix description here
```

---

### Step 5.2: Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ src/*.egg-info

# Verify they're gone
ls dist/  # Should show: No such file or directory
```

---

### Step 5.3: Build Using Script (Recommended)

```bash
# Run the automated build script
./build.sh

# This script:
# 1. Cleans old builds
# 2. Installs dependencies
# 3. Formats code
# 4. Runs linter
# 5. Builds package
# 6. Verifies package

# Output should end with:
# ✨ Build successful! Files created:
# -rw-r--r--  1 user  group  15K  rl_autoscale-1.0.0-py3-none-any.whl
# -rw-r--r--  1 user  group  12K  rl_autoscale-1.0.0.tar.gz
```

---

### Step 5.4: Build Manually (Alternative)

```bash
# Install build tools if needed
uv pip install --system build

# Build the package
uv run python -m build

# Creates two files in dist/:
# - rl_autoscale-1.0.0-py3-none-any.whl (wheel)
# - rl_autoscale-1.0.0.tar.gz (source)
```

---

### Step 5.5: Verify the Build

```bash
# Install twine if needed
uv pip install --system twine

# Check package metadata and format
twine check dist/*

# Should show:
# Checking dist/rl_autoscale-1.0.0-py3-none-any.whl: PASSED
# Checking dist/rl_autoscale-1.0.0.tar.gz: PASSED
```

---

## 6. Testing the Build

### Step 6.1: Create Test Environment

```bash
# Create a separate test environment
cd /tmp
python -m venv test_env
source test_env/bin/activate
```

---

### Step 6.2: Reinstall Dependencies
```bash
# If you have old venv, remove it
rm -rf venv .venv uv.lock

# Setup everything with one command (super fast!)
        # uv sync --all-extras   # ❌ Fails: no pyproject.toml here

# That's it! UV handles everything automatically.
```
The previous version of this guide incorrectly suggested running `uv sync` **after** switching to `/tmp`. That fails because `uv sync` looks for a `pyproject.toml` in the current (or parent) directory, which does not exist in `/tmp`.

You have two GOOD options to install the package into this fresh test environment:

#### Option A: Install the built artifacts (recommended realism test)
Use this if you've already run the build in Step 5 and have files in `dist/`.

```bash
# (Still inside the fresh /tmp/test_env virtualenv)
pip install --upgrade pip

# Install from wheel (preferred) – adjust the version if different
pip install ~/Documents/code/rl-autoscale/dist/rl_autoscale-*.whl

# Or install from the source tarball
# pip install ~/Documents/code/rl-autoscale/dist/rl_autoscale-*.tar.gz

# If you want optional extras (flask / fastapi) for integration tests:
# Default: fetch from PyPI (recommended)
pip install 'rl-autoscale[flask,fastapi]'

# Or install the frameworks explicitly
pip install flask fastapi uvicorn

# Offline variant (advanced): only if you have all required wheels
# for Flask/FastAPI and their dependencies placed in the directory below.
# pip install 'rl-autoscale[flask,fastapi]' --no-index \
#     --find-links ~/Documents/code/rl-autoscale/dist/
```

Explanation:
- Using the wheel mimics what end users get from PyPI.
- If you need Flask/FastAPI, prefer installing extras from PyPI as shown above.
- The offline `--no-index` approach only works if you provide local wheels for Flask/FastAPI and all their transitive dependencies.

Tip: You can add extras after installing the base wheel by running:
```bash
pip install 'rl-autoscale[flask,fastapi]'
```

#### Option B: Install directly from the source tree (editable or standard)
This is useful if you want to confirm an editable install works cleanly in a brand‑new env.

```bash
# Standard (non-editable) install from source path
pip install ~/Documents/code/rl-autoscale

# With extras
pip install '~/Documents/code/rl-autoscale[flask,fastapi]'

# Editable install (only if you really need live code changes)
pip install -e '~/Documents/code/rl-autoscale[flask,fastapi]'
```

#### Option C: Use uv just for installation (not sync)
`uv sync` must be run from the project root. In a throwaway test env elsewhere, prefer `pip` or `uv pip install`:

```bash
uv pip install ~/Documents/code/rl-autoscale/dist/rl_autoscale-*.whl
# Or with extras directly from source
uv pip install '~/Documents/code/rl-autoscale[flask,fastapi]'
```

---

### Step 6.3: Test Imports

```bash
# Test basic import
python -c "from rl_autoscale import enable_metrics; print('✓ Import works!')"

# Test all exports
python -c "
from rl_autoscale import (
    enable_metrics,
    enable_flask_metrics,
    enable_fastapi_metrics,
    RLMetrics,
    get_metrics_registry
)
print('✓ All imports work!')
"
```

---

### Step 6.4: Test Flask Integration

```bash
# Install Flask
pip install flask

# Create test file
cat > test_flask.py << 'EOF'
from flask import Flask
from rl_autoscale import enable_metrics

app = Flask(__name__)
enable_metrics(app, port=8000)

@app.route("/test")
def test():
    return "Works!"

if __name__ == "__main__":
    print("✓ Flask integration works!")
    print("Visit: http://localhost:5000/test")
    print("Metrics: http://localhost:8000/metrics")
    app.run()
EOF

# Run test
python test_flask.py
```

---

### Step 6.5: Test FastAPI Integration

```bash
# Install FastAPI
pip install fastapi uvicorn

# Create test file
cat > test_fastapi.py << 'EOF'
from fastapi import FastAPI
from rl_autoscale import enable_metrics

app = FastAPI()
enable_metrics(app, port=8001)

@app.get("/test")
def test():
    return {"status": "works"}

if __name__ == "__main__":
    import uvicorn
    print("✓ FastAPI integration works!")
    print("Visit: http://localhost:8000/test")
    print("Metrics: http://localhost:8001/metrics")
    uvicorn.run(app)
EOF

# Run test
python test_fastapi.py
```

---

### Step 6.6: Cleanup Test Environment

```bash
# Deactivate and remove test environment
deactivate
cd ~/Documents/code/rl-autoscale
rm -rf /tmp/test_env /tmp/test_*.py
```

---

## 7. Publishing to Test PyPI

### Step 7.1: Create Test PyPI Account

1. Go to: https://test.pypi.org/account/register/
2. Fill in your details
3. Verify your email
4. Login to Test PyPI

---

### Step 7.2: Create API Token (Test PyPI)

1. Go to: https://test.pypi.org/manage/account/#api-tokens
2. Click "Add API token"
3. Token name: `rl-autoscale-upload`
4. Scope: "Entire account" (for first upload)
5. Click "Add token"
6. **Copy the token** (starts with `pypi-`)

---

### Step 7.3: Configure Token

**Option A: Using environment variable (temporary)**
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-TEST-PYPI-TOKEN-HERE
```

**Option B: Using .pypirc file (permanent)**
```bash
# Create ~/.pypirc
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-PYPI-TOKEN-HERE

[pypi]
username = __token__
password = pypi-YOUR-REAL-PYPI-TOKEN-HERE
EOF

# Secure the file
chmod 600 ~/.pypirc
```

---

### Step 7.4: Upload to Test PyPI

```bash
# Upload
twine upload --repository testpypi dist/*

# Or if using .pypirc:
twine upload -r testpypi dist/*

# Output should show:
# Uploading distributions to https://test.pypi.org/legacy/
# Uploading rl_autoscale-1.0.0-py3-none-any.whl
# Uploading rl_autoscale-1.0.0.tar.gz
#
# View at:
# https://test.pypi.org/project/rl-autoscale/1.0.0/
```

---

### Step 7.5: Test Installation from Test PyPI

```bash
# Create test environment
cd /tmp
python -m venv testpypi_env
source testpypi_env/bin/activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    'rl-autoscale[flask]'

# Note (zsh): quote requirement specifiers with extras to avoid globbing errors.
# For multiple extras, use e.g. 'rl-autoscale[flask,fastapi]'.

# Test it
python -c "from rl_autoscale import enable_metrics; print('✓ Test PyPI works!')"

# Cleanup
deactivate
rm -rf /tmp/testpypi_env
```

---

## 8. Publishing to PyPI

### Step 8.1: Create PyPI Account

1. Go to: https://pypi.org/account/register/
2. Fill in your details
3. Verify your email
4. Login to PyPI

---

### Step 8.2: Create API Token (PyPI)

1. Go to: https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `rl-autoscale-upload`
4. Scope: "Entire account" (for first upload, then project-specific)
5. Click "Add token"
6. **Copy the token** (starts with `pypi-`)

---

### Step 8.3: Final Pre-Publish Checklist

```bash
# 1. All tests pass
uv run pytest
# ✓ All passed

# 2. Code is formatted
ruff format --check .
# ✓ All files formatted

# 3. No linting issues
ruff check .
# ✓ All checks passed

# 4. Build is clean
ls dist/
# ✓ Should show .whl and .tar.gz

# 5. Package verified
twine check dist/*
# ✓ PASSED

# 6. Version is correct
grep version pyproject.toml
grep __version__ src/rl_autoscale/__init__.py
# ✓ Both match

# 7. CHANGELOG updated
cat CHANGELOG.md
# ✓ Has entry for new version

# 8. Git is clean
git status
# ✓ All changes committed
```

---

### Step 8.4: Upload to PyPI

```bash
# Upload (THIS IS THE REAL THING!)
twine upload dist/*

# You'll be prompted for credentials:
# Enter your username: __token__
# Enter your password: pypi-YOUR-REAL-TOKEN-HERE

# Or use environment variables:
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-REAL-TOKEN-HERE
twine upload dist/*

# Output should show:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading rl_autoscale-1.0.0-py3-none-any.whl
# Uploading rl_autoscale-1.0.0.tar.gz
#
# View at:
# https://pypi.org/project/rl-autoscale/1.0.0/
```

---

### Step 8.5: Verify on PyPI

1. **Visit PyPI page**: https://pypi.org/project/rl-autoscale/
2. Check that:
   - ✓ Version is correct
   - ✓ Description renders properly
   - ✓ README is displayed
   - ✓ Links work
   - ✓ Classifiers are correct

---

### Step 8.6: Test Installation from PyPI

```bash
# Create fresh environment
cd /tmp
python -m venv pypi_test
source pypi_test/bin/activate

# Install from PyPI (THE REAL DEAL!)
pip install rl-autoscale[flask]

# Test it
python -c "
from rl_autoscale import enable_metrics
print('✓ PyPI installation works!')
print('🎉 Successfully published to PyPI!')
"

# Test version
python -c "import rl_autoscale; print(f'Version: {rl_autoscale.__version__}')"

# Cleanup
deactivate
rm -rf /tmp/pypi_test
```

---

## 9. Post-Publishing

### Step 9.1: Create Git Tag

```bash
cd ~/Documents/code/rl-autoscale

# Create and push tag
git tag v1.0.0
git push origin v1.0.0

# Verify tag
git tag -l
```

---

### Step 9.2: Automated Publishing with GitHub Actions (Recommended)

**This is the modern, secure way to publish!**

The repository includes a production-ready GitHub Actions workflow that uses **Trusted Publishers** (OIDC) for token-free publishing.

#### Benefits:
- ✅ No API tokens to manage or leak
- ✅ Automatic publishing on git tags
- ✅ Runs tests before every publish
- ✅ Publishes to Test PyPI on every push
- ✅ Creates GitHub Releases automatically
- ✅ Signs artifacts with Sigstore

#### One-Time Setup (5 minutes):

**1. Create GitHub Environments:**
- Go to repo Settings → Environments
- Create `pypi` (with manual approval required)
- Create `testpypi` (no approval needed)

**2. Configure Trusted Publishers on PyPI:**

For PyPI:
- Visit: https://pypi.org/manage/account/publishing/
- Add pending publisher:
  - Project: `rl-autoscale`
  - Owner: `ghazafm`
  - Repo: `rl-autoscale`
  - Workflow: `publish.yml`
  - Environment: `pypi`

For Test PyPI:
- Visit: https://test.pypi.org/manage/account/publishing/
- Add pending publisher (same details, but environment: `testpypi`)

**3. Publish a new version:**

```bash
# Update versions in pyproject.toml, __init__.py, CHANGELOG.md
# Then:
git add .
git commit -m "Release v1.0.1"
git tag v1.0.1
git push origin master --tags

# GitHub Actions automatically:
# - Builds package
# - Runs tests
# - Publishes to Test PyPI
# - Publishes to PyPI (after approval)
# - Creates GitHub Release
```

**Detailed setup guide**: See `PUBLISHING.md`

---

### Step 9.3: Create GitHub Release (Manual Alternative)

If not using automated publishing:

1. Go to: https://github.com/ghazafm/rl-autoscale/releases/new
2. Click "Choose a tag" → Select `v1.0.0`
3. Release title: `v1.0.0 - Initial Release`
4. Description: Copy from `CHANGELOG.md`
5. Check "Set as the latest release"
6. Click "Publish release"

**Note**: If using the GitHub Actions workflow, releases are created automatically!

---

### Step 9.4: Monitor Deployment

**If using GitHub Actions:**
- Actions tab: https://github.com/ghazafm/rl-autoscale/actions
- Test PyPI: https://test.pypi.org/project/rl-autoscale/
- Production PyPI: https://pypi.org/project/rl-autoscale/

**Check PyPI stats:**
- Visit: https://pypistats.org/packages/rl-autoscale

**Monitor GitHub activity:**
- Visit: https://github.com/ghazafm/rl-autoscale/pulse

---

### Step 9.5: Respond to Issues

---

### Step 9.5: Update Project Links

Watch for:
- Installation issues
- Bug reports
- Feature requests
- Questions

Respond promptly to build community trust!

---

## 10. Troubleshooting

### Problem: 403 "Invalid or non-existent authentication information" on Test PyPI

You may see:

```
HTTPError: 403 Forbidden from https://test.pypi.org/legacy/
Invalid or non-existent authentication information.
```

Fixes to try (in order):

1) Use a Test PyPI token (not a production PyPI token)
- Create it at: https://test.pypi.org/manage/account/#api-tokens
- Username must be `__token__`; password is the Test PyPI token (starts with `pypi-`).

2) Upload to the correct repository
```bash
twine upload --repository testpypi dist/*
```
This targets https://test.pypi.org/legacy/.

3) Ensure token scope is sufficient
- For the first-ever upload of this project on Test PyPI, use scope "Entire account". Project-scoped tokens only work after the project already exists and must match the exact project name.

4) Quote your token and avoid mixed configs
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD='pypi-YOUR-TEST-PYPI-TOKEN-HERE'
twine upload --repository testpypi dist/*
```
Twine precedence is: command options > environment variables > ~/.pypirc. Avoid pointing different sources at different repos.

5) Optional: ~/.pypirc for Test PyPI
```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-PYPI-TOKEN-HERE
EOF
chmod 600 ~/.pypirc

twine upload -r testpypi dist/*
```

6) If the project name is taken on Test PyPI
- If `rl-autoscale` is already claimed by someone else on Test PyPI, temporarily change the `project.name` in `pyproject.toml` to a unique name (e.g., `rl-autoscale-test`), rebuild, and upload.

### Problem: "Module not found" when testing

**Solution:**
```bash
# Reinstall in editable mode
uv pip install -e .
```

---

### Problem: "File already exists" on PyPI upload

**Cause:** You can't re-upload the same version to PyPI.

**Solution:**
```bash
# Bump version in pyproject.toml and __init__.py
# Then rebuild and upload
```

---

### Problem: Tests fail with import errors

**Solution:**
```bash
# Install with all extras
uv pip install -e ".[dev,flask,fastapi]"
```

---

### Problem: Package includes wrong files

**Solution:**
```bash
# Check MANIFEST.in
cat MANIFEST.in

# Check what's included in build
tar -tzf dist/rl_autoscale-1.0.0.tar.gz

# Fix MANIFEST.in if needed
```

---

### Problem: README not rendering on PyPI

**Cause:** Markdown syntax error or unsupported features.

**Solution:**
```bash
# Validate README
python -m readme_renderer README.md -o /tmp/out.html

# Check output
open /tmp/out.html
```

---

### Problem: Import works locally but fails after pip install

**Cause:** Package structure issue.

**Solution:**
```bash
# Verify pyproject.toml
cat pyproject.toml | grep -A5 "packages.find"

# Should show:
# [tool.setuptools.packages.find]
# where = ["src"]
# include = ["rl_autoscale*"]
```

---

### Problem: UV not found after install

**Solution:**
```bash
# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Add to shell config
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc

# Restart terminal
```

---

## 📝 Quick Reference

### Daily Development
```bash
ruff format . && ruff check . && uv run pytest
```

### Before Commit
```bash
git status
ruff format --check .
ruff check .
uv run pytest
git add .
git commit -m "Your message"
git push
```

### Release New Version
```bash
# 1. Update versions (3 files)
# 2. Update CHANGELOG.md
# 3. Build and test
./build.sh
# 4. Git commit and tag
git commit -am "Release v1.0.1"
git tag v1.0.1
git push && git push --tags
# 5. Upload to PyPI
twine upload dist/*
# 6. Create GitHub Release
```

---

## 🎯 Next Steps After First Publish

1. ✅ Add PyPI badge to README
2. ✅ Share on social media
3. ✅ Write blog post about your package
4. ✅ Submit to awesome lists
5. ✅ Monitor issues and respond
6. ✅ Plan next version features

---

## 🎉 Congratulations!

You've successfully:
- ✅ Set up modern Python development with UV + Ruff
- ✅ Built a production-ready package
- ✅ Published to PyPI
- ✅ Shared your work with the world!

**Your package is now available worldwide:**
```bash
pip install rl-autoscale
```

🚀 **You're now a published Python package author!**
