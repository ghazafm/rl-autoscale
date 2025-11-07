# Production-Ready PyPI Publishing Guide

This document provides step-by-step instructions for publishing `rl-autoscale` to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both [Test PyPI](https://test.pypi.org/account/register/) and [PyPI](https://pypi.org/account/register/)

2. **Install Build Tools**:
   ```bash
   pip install build twine
   ```

3. **API Tokens**: Create API tokens for authentication:
   - Test PyPI: https://test.pypi.org/manage/account/#api-tokens
   - PyPI: https://pypi.org/manage/account/token/

## Pre-Publishing Checklist

Before publishing, ensure:

- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `black .`
- [ ] Linting passes: `ruff check .`
- [ ] Version number updated in:
  - [ ] `pyproject.toml`
  - [ ] `src/rl_autoscale/__init__.py`
  - [ ] `CHANGELOG.md`
- [ ] README.md is up to date
- [ ] CHANGELOG.md has entry for new version
- [ ] All changes committed to git
- [ ] Git tag created: `git tag v1.0.0`

## Manual Publishing (First Time)

### 1. Clean Previous Builds

```bash
rm -rf dist/ build/ src/*.egg-info
```

### 2. Build the Package

```bash
python -m build
```

This creates:
- `dist/rl_autoscale-1.0.0.tar.gz` (source distribution)
- `dist/rl_autoscale-1.0.0-py3-none-any.whl` (wheel)

### 3. Check the Build

```bash
twine check dist/*
```

Should output: `Checking dist/... PASSED`

### 4. Test on Test PyPI (Recommended First)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Enter your Test PyPI credentials when prompted
# Or set up token in ~/.pypirc (see below)
```

Test the installation:
```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ rl-autoscale

# Test it works
python -c "from rl_autoscale import enable_metrics; print('Success!')"

deactivate
rm -rf test_env
```

### 5. Publish to PyPI

Once testing is successful:

```bash
twine upload dist/*
```

### 6. Verify on PyPI

Visit: https://pypi.org/project/rl-autoscale/

Install and test:
```bash
pip install rl-autoscale
python -c "from rl_autoscale import enable_metrics; print('Production Success!')"
```

## Automated Publishing with GitHub Actions (Recommended)

The repository includes a production-ready GitHub Actions workflow (`.github/workflows/publish.yml`) that uses **Trusted Publishers** (OIDC) for secure, token-free publishing.

### Why Trusted Publishers?

✅ **Security**: No long-lived API tokens to leak or rotate
✅ **Simplicity**: Zero manual token management
✅ **Modern**: Uses OpenID Connect (OIDC) standard
✅ **Automated**: GitHub authenticates directly with PyPI

### One-Time Setup (5 minutes)

#### Step 1: Configure GitHub Environments

1. Go to your repo Settings → Environments
2. Create two environments:

**Environment: `pypi`** (production)
- Add protection rule: "Required reviewers" (yourself)
- This prevents accidental production releases

**Environment: `testpypi`** (testing)
- No protection rules needed (publishes on every push to master)

#### Step 2: Configure PyPI Trusted Publishers

**For PyPI (production):**
1. Go to: https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `rl-autoscale`
   - **Owner**: `ghazafm`
   - **Repository name**: `rl-autoscale`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Click "Add"

**For Test PyPI (staging):**
1. Go to: https://test.pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `rl-autoscale`
   - **Owner**: `ghazafm`
   - **Repository name**: `rl-autoscale`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `testpypi`
4. Click "Add"

**Important Notes:**
- If the project already exists on PyPI, go to the project settings instead: https://pypi.org/manage/project/rl-autoscale/settings/publishing/
- The "pending publisher" will activate on first successful publish
- No API tokens needed anywhere!

### How the Workflow Works

**On every push to `master`:**
1. ✅ Builds the package
2. ✅ Runs linters (ruff format, ruff check)
3. ✅ Runs tests with coverage
4. ✅ Publishes to **Test PyPI** automatically

**On tag push (e.g., `v1.0.1`):**
1. ✅ All of the above, plus:
2. ✅ Publishes to **PyPI** (production)
3. ✅ Creates GitHub Release with signed artifacts
4. ✅ Attaches distribution files to release

### Publishing a New Version

#### Quick Release (Tag-based)

```bash
# 1. Update version in 3 files:
#    - pyproject.toml
#    - src/rl_autoscale/__init__.py
#    - CHANGELOG.md

# 2. Commit and tag
git add .
git commit -m "Release v1.0.1"
git tag v1.0.1
git push origin master --tags

# 3. GitHub Actions does the rest!
#    - Builds
#    - Tests
#    - Publishes to Test PyPI
#    - Publishes to PyPI (after manual approval in pypi environment)
#    - Creates GitHub Release
```

#### Using GitHub Releases UI (Alternative)

```bash
# 1. Update versions and commit
git add .
git commit -m "Release v1.0.1"
git push

# 2. Create tag
git tag v1.0.1
git push origin v1.0.1

# 3. Create release on GitHub:
# - Go to: https://github.com/ghazafm/rl-autoscale/releases/new
# - Choose tag: v1.0.1
# - Title: v1.0.1
# - Description: Copy from CHANGELOG.md
# - Publish release
#
# Workflow triggers automatically!
```

### Monitoring Builds

- **Actions Tab**: https://github.com/ghazafm/rl-autoscale/actions
- **Test PyPI**: https://test.pypi.org/project/rl-autoscale/
- **Production PyPI**: https://pypi.org/project/rl-autoscale/

### What Gets Published

**Pull Requests to master:**
- → Build and test only (no publishing)
- → Validates code quality before merge

**Every push to master:**
- → Test PyPI (automatic, no approval needed)

**Tagged commits (v*):**
- → Test PyPI (automatic)
- → PyPI (requires manual approval in `pypi` environment)
- → GitHub Release with signed artifacts

### Testing Before Production

The workflow automatically publishes to Test PyPI first. Test it:

```bash
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  'rl-autoscale[flask]'

python -c "from rl_autoscale import enable_metrics; print('✓ Works')"
```

### Security Features

1. **OIDC Authentication**: No tokens in repo secrets
2. **Sigstore Signing**: Artifacts signed cryptographically
3. **Environment Protection**: Manual approval for production
4. **Minimal Permissions**: Only `id-token: write` granted
5. **PEP 740 Attestations**: Auto-generated provenance

### Alternative: API Tokens (Not Recommended)

If you can't use Trusted Publishers:

1. Create tokens:
   - PyPI: https://pypi.org/manage/account/token/
   - Test PyPI: https://test.pypi.org/manage/account/#api-tokens

2. Add to GitHub Secrets (Settings → Secrets → Actions):
   - `PYPI_API_TOKEN`
   - `TEST_PYPI_API_TOKEN`

3. Update workflow to use:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

**But seriously, use Trusted Publishers instead!**

## Configuration: ~/.pypirc

Create `~/.pypirc` for storing credentials (optional):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-API-TOKEN-HERE
```

Secure it:
```bash
chmod 600 ~/.pypirc
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backward compatible

## Common Issues

### "File already exists"
PyPI doesn't allow re-uploading the same version. Increment version number.

### Import errors after publishing
Check `[tool.setuptools.packages.find]` in `pyproject.toml` includes correct paths.

### Missing dependencies
Ensure `dependencies` in `pyproject.toml` lists all required packages.

### Large package size
Check `.gitignore` and `MANIFEST.in` to exclude unnecessary files.

## Post-Publishing Checklist

After successful publish:

- [ ] Test installation: `pip install rl-autoscale`
- [ ] Check PyPI page renders correctly
- [ ] Update documentation if needed
- [ ] Announce on relevant channels
- [ ] Create GitHub release with changelog
- [ ] Update project status badge (if any)

## Rolling Back

If you need to yank a release:

```bash
# Yank from PyPI (keeps files but marks as bad)
twine upload --repository pypi --skip-existing dist/*

# Or via PyPI web interface:
# Go to https://pypi.org/project/rl-autoscale/
# → Manage → Releases → Select version → Yank
```

Note: Yanked versions can still be installed with explicit version, but won't be installed by default.

## Support

For issues with publishing:
- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
