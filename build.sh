#!/bin/bash
# Quick test and build script for rl-autoscale

set -e

echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ src/*.egg-info

echo "📦 Installing dependencies..."
if command -v uv &> /dev/null; then
    echo "✓ Using uv (fast!)"
    uv pip install --system build twine ruff
else
    echo "⚠️  uv not found, using pip (install uv: curl -LsSf https://astral.sh/uv/install.sh | sh)"
    pip install -q build twine ruff
fi

echo "🎨 Formatting code..."
ruff format .

echo "🔍 Running linter..."
ruff check . || echo "⚠️  Ruff warnings (review but not blocking)"

echo "🏗️  Building package..."
python -m build

echo "✅ Checking package..."
twine check dist/*

echo ""
echo "✨ Build successful! Files created:"
ls -lh dist/

echo ""
echo "📝 Next steps:"
echo "  1. Test locally: pip install dist/*.whl"
echo "  2. Test on Test PyPI: twine upload --repository testpypi dist/*"
echo "  3. Publish to PyPI: twine upload dist/*"
echo ""
echo "Or use GitHub Actions by creating a release!"
