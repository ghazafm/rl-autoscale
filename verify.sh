#!/bin/bash
# Verification script for production readiness

echo "🔍 RL-Autoscale Production Readiness Check"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check directory structure
echo "📁 Directory Structure"
echo "---"

if [ -d "src/rl_autoscale" ]; then
    check_pass "src/rl_autoscale/ directory exists"
else
    check_fail "src/rl_autoscale/ directory missing"
fi

if [ -d "tests" ]; then
    check_pass "tests/ directory exists"
else
    check_fail "tests/ directory missing"
fi

if [ -d ".github/workflows" ]; then
    check_pass ".github/workflows/ directory exists"
else
    check_fail ".github/workflows/ directory missing"
fi

echo ""

# Check required files
echo "📄 Required Files"
echo "---"

required_files=(
    "pyproject.toml"
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "src/rl_autoscale/__init__.py"
    "src/rl_autoscale/py.typed"
    ".gitignore"
    "MANIFEST.in"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        check_pass "$file"
    else
        check_fail "$file missing"
    fi
done

echo ""

# Check Python module structure
echo "🐍 Python Module Structure"
echo "---"

if grep -q "where = \[\"src\"\]" pyproject.toml; then
    check_pass "pyproject.toml: src layout configured"
else
    check_fail "pyproject.toml: src layout not configured"
fi

if grep -q "__version__" src/rl_autoscale/__init__.py; then
    check_pass "__init__.py: version defined"
else
    check_fail "__init__.py: version not defined"
fi

if grep -q "__all__" src/rl_autoscale/__init__.py; then
    check_pass "__init__.py: __all__ defined"
else
    check_fail "__init__.py: __all__ not defined"
fi

echo ""

# Check package metadata
echo "📦 Package Metadata"
echo "---"

if grep -q "name = \"rl-autoscale\"" pyproject.toml; then
    check_pass "Package name: rl-autoscale"
else
    check_fail "Package name not set correctly"
fi

if grep -q "prometheus-client" pyproject.toml; then
    check_pass "Core dependency: prometheus-client"
else
    check_fail "Core dependency missing"
fi

if grep -q "\[project.optional-dependencies\]" pyproject.toml; then
    check_pass "Optional dependencies defined"
else
    check_warn "No optional dependencies"
fi

echo ""

# Check CI/CD
echo "🚀 CI/CD Configuration"
echo "---"

if [ -f ".github/workflows/ci.yml" ]; then
    check_pass "CI workflow configured"
else
    check_fail "CI workflow missing"
fi

if [ -f ".github/workflows/publish.yml" ]; then
    check_pass "Publish workflow configured"
else
    check_fail "Publish workflow missing"
fi

echo ""

# Check documentation
echo "📚 Documentation"
echo "---"

docs=(
    "CONTRIBUTING.md"
    "SECURITY.md"
    "PUBLISHING.md"
    "PROJECT_STRUCTURE.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        check_pass "$doc"
    else
        check_warn "$doc not found"
    fi
done

echo ""

# Check test structure
echo "🧪 Test Structure"
echo "---"

test_files=(
    "tests/__init__.py"
    "tests/conftest.py"
    "tests/test_metrics.py"
    "tests/test_flask_middleware.py"
    "tests/test_fastapi_middleware.py"
    "tests/test_auto_detection.py"
)

for test in "${test_files[@]}"; do
    if [ -f "$test" ]; then
        check_pass "$test"
    else
        check_warn "$test not found"
    fi
done

echo ""
echo "=========================================="
echo "✨ Production Readiness Check Complete!"
echo ""
echo "📝 Next Steps:"
echo "  1. Run: pip install -e \".[dev,flask,fastapi]\""
echo "  2. Run: pytest"
echo "  3. Run: black ."
echo "  4. Run: ruff check ."
echo "  5. Run: ./build.sh"
echo "  6. Test installation: pip install dist/*.whl"
echo "  7. Ready for PyPI! 🎉"
echo ""
