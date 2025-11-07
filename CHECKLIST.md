# ✅ Complete Checklist: Development to PyPI

Quick checklist version of the complete workflow. Check off items as you go!

---

## 🔧 Initial Setup (One-Time)

```bash
# □ 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# □ 2. Clone/Navigate to project
cd ~/Documents/code/rl-autoscale

# □ 3. Setup everything (one command!)
uv sync --all-extras

# □ 4. Verify setup
./verify.sh
```

**✅ Setup complete!**

---

## 💻 Daily Development

```bash
# □ 1. Make code changes
# Edit files in src/rl_autoscale/

# □ 2. Format code
ruff format .

# □ 3. Check linting
ruff check .

# □ 4. Auto-fix issues
ruff check . --fix

# □ 5. Run tests
uv run pytest

# □ 6. Check coverage
uv run pytest --cov=rl_autoscale
```

**✅ Development cycle complete!**

---

## 🧪 Testing Checklist

```bash
# □ 1. Run all tests
uv run pytest

# □ 2. Run with coverage
uv run pytest --cov=rl_autoscale --cov-report=html

# □ 3. Check coverage report
open htmlcov/index.html

# □ 4. Run specific tests
uv run pytest tests/test_metrics.py

# □ 5. Test examples
uv run python example_flask.py
uv run python example_fastapi.py
```

**Target: >80% coverage, all tests passing ✅**

---

## 📦 Build Checklist

```bash
# □ 1. Clean previous builds
rm -rf dist/ build/ src/*.egg-info

# □ 2. Format code
ruff format .

# □ 3. Check linting
ruff check .

# □ 4. Run tests
uv run pytest

# □ 5. Build package
uv run python -m build

# □ 6. Verify package
twine check dist/*
```

**Or use the shortcut:**
```bash
# □ Run build script
./build.sh
```

**✅ Package built successfully!**

---

## 🔬 Test Build Locally

```bash
# □ 1. Create test environment
cd /tmp && python -m venv test_env && source test_env/bin/activate

# □ 2. Install built package
pip install ~/Documents/code/rl-autoscale/dist/rl_autoscale-*.whl

# □ 3. Test imports
python -c "from rl_autoscale import enable_metrics; print('✓ Works!')"

# □ 4. Test Flask integration
pip install flask
# Create and run test Flask app

# □ 5. Test FastAPI integration
pip install fastapi uvicorn
# Create and run test FastAPI app

# □ 6. Cleanup
deactivate && cd ~/Documents/code/rl-autoscale && rm -rf /tmp/test_env
```

**✅ Local testing complete!**

---

## 🧪 Test PyPI (Optional but Recommended)

```bash
# □ 1. Create Test PyPI account
# Visit: https://test.pypi.org/account/register/

# □ 2. Create API token
# Visit: https://test.pypi.org/manage/account/#api-tokens

# □ 3. Upload to Test PyPI
twine upload --repository testpypi dist/*

# □ 4. Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    rl-autoscale

# □ 5. Verify it works
python -c "from rl_autoscale import enable_metrics; print('✓')"
```

**✅ Test PyPI verified!**

---

## 🚀 Publish to PyPI

### Pre-Publish Checklist

```bash
# Code Quality
# □ All tests pass: uv run pytest
# □ Code formatted: ruff format --check .
# □ No lint issues: ruff check .
# □ Coverage >80%: uv run pytest --cov=rl_autoscale

# Package
# □ Build clean: ls dist/
# □ Package verified: twine check dist/*

# Version
# □ Version in pyproject.toml updated
# □ Version in __init__.py updated
# □ CHANGELOG.md updated

# Git
# □ All changes committed: git status
# □ Working on master/main branch: git branch
```

### Publishing Steps

```bash
# □ 1. Create PyPI account
# Visit: https://pypi.org/account/register/

# □ 2. Create API token
# Visit: https://pypi.org/manage/account/token/

# □ 3. Set credentials
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-TOKEN-HERE

# □ 4. Upload to PyPI (REAL!)
twine upload dist/*

# □ 5. Verify on PyPI
# Visit: https://pypi.org/project/rl-autoscale/

# □ 6. Test installation
pip install rl-autoscale
python -c "from rl_autoscale import enable_metrics; print('✅ Published!')"
```

**🎉 Published to PyPI!**

---

## 📝 Post-Publishing

```bash
# □ 1. Create Git tag
git tag v1.0.0
git push origin v1.0.0

# □ 2. Create GitHub Release
# Visit: https://github.com/ghazafm/rl-autoscale/releases/new

# □ 3. Update badges in README
# Add PyPI version badge

# □ 4. Share announcement
# Twitter, LinkedIn, Reddit, etc.

# □ 5. Monitor initial usage
# Check issues, stars, downloads
```

**✅ Release complete!**

---

## 🔄 Release New Version

```bash
# □ 1. Update version numbers (3 files)
# - pyproject.toml: version = "1.0.1"
# - src/rl_autoscale/__init__.py: __version__ = "1.0.1"
# - CHANGELOG.md: Add new section

# □ 2. Commit changes
git add .
git commit -m "Release v1.0.1"

# □ 3. Build
./build.sh

# □ 4. Tag and push
git tag v1.0.1
git push && git push --tags

# □ 5. Upload to PyPI
twine upload dist/*

# □ 6. Create GitHub Release
# Visit GitHub and create release from tag
```

**✅ New version released!**

---

## 📊 Quality Metrics

Track these metrics for your package:

```
Development
□ Code Coverage: >80%
□ All Tests: Passing
□ Lint Issues: 0
□ Format: Consistent

Package
□ Build: Successful
□ Twine Check: PASSED
□ Size: Reasonable (<1MB)

PyPI
□ Installation: Works
□ README: Renders
□ Links: All working
□ Downloads: Growing
```

---

## 🐛 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Import error | `uv pip install -e .` |
| Tests fail | `uv pip install -e ".[dev,flask,fastapi]"` |
| UV not found | `export PATH="$HOME/.cargo/bin:$PATH"` |
| File exists (PyPI) | Bump version number |
| Format issues | `ruff format .` |
| Lint errors | `ruff check . --fix` |
| Build fails | Clean: `rm -rf dist/ build/` |

---

## ⚡ One-Line Commands

```bash
# Complete development cycle
ruff format . && ruff check . && uv run pytest

# Quick build and verify
rm -rf dist/ && uv run python -m build && twine check dist/*

# Format, lint, test, build
./build.sh

# Full pre-commit check
ruff format --check . && ruff check . && uv run pytest && echo "✅ Ready to commit!"

# Full pre-publish check
./build.sh && twine check dist/* && echo "✅ Ready to publish!"
```

---

## 📚 Documentation Quick Links

- **Complete Guide**: [STEP_BY_STEP.md](STEP_BY_STEP.md)
- **UV Guide**: [UV_GUIDE.md](UV_GUIDE.md)
- **Quick Reference**: [QUICKREF.md](QUICKREF.md)
- **Publishing Guide**: [PUBLISHING.md](PUBLISHING.md)
- **Migration Info**: [MIGRATION_TO_UV.md](MIGRATION_TO_UV.md)

---

## 🎯 Current Status

Mark your progress:

```
Setup Phase
□ UV installed
□ Project cloned
□ Dependencies installed
□ Tests passing

Development Phase
□ Code written
□ Tests added
□ Documentation updated
□ Examples working

Build Phase
□ Code formatted
□ Linting clean
□ Tests passing
□ Package built

Publishing Phase
□ Test PyPI successful
□ PyPI account created
□ Token configured
□ Published to PyPI

Post-Release Phase
□ Git tagged
□ GitHub Release created
□ Announcement shared
□ Monitoring setup
```

---

## 🎉 Success Criteria

Your package is ready when ALL are ✅:

- ✅ All tests pass
- ✅ Code coverage >80%
- ✅ No linting errors
- ✅ Code formatted consistently
- ✅ Build successful
- ✅ Package verified with twine
- ✅ Test installation works
- ✅ Version numbers consistent
- ✅ CHANGELOG updated
- ✅ Git committed and tagged
- ✅ Documentation complete

**Then you're ready to publish! 🚀**

---

**Print this checklist and mark items as you complete them!**
