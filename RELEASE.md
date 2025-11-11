# Release Guide for hot-spot-analysis

## Version 1.1.0 Release Instructions

### Overview

Version 1.1.0 introduces comprehensive refactoring with dictionary/JSON optimizations:
- Direct dictionary creation (no temporary columns)
- List comprehension optimizations across the codebase
- Deprecated `lists_to_dict()` function with migration guidance
- ~28 lines of code removed, improved performance
- 100% backward compatible

---

## Quick Release (Production)

```bash
# 1. Clean previous builds
rm -rf dist/ build/ *.egg-info src/*.egg-info

# 2. Build distribution packages
python -m build

# 3. Upload to PyPI
python -m twine upload dist/*

# 4. Tag and create GitHub release
git tag -a v1.1.0 -m "Release version 1.1.0: Dictionary/JSON optimizations"
git push origin v1.1.0
```

---

## Detailed Release Process

### Prerequisites

Install required build tools:

```bash
pip install --upgrade build twine
```

Configure PyPI credentials in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TEST-API-TOKEN-HERE
```

### Step-by-Step Instructions

#### 1. Clean Previous Builds

Remove any old build artifacts to ensure a fresh build:

```bash
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Verify clean state
ls -la dist/ 2>/dev/null || echo "dist/ directory is clean"
```

#### 2. Run Tests

Ensure all tests pass before building:

```bash
python -m pytest tests/ -v

# Expected output:
# ======================== 14 passed, 1 warning in 1.05s ========================
```

#### 3. Build Distribution Packages

Build both source distribution and wheel:

```bash
python -m build

# This creates:
# - dist/hot_spot_analysis-1.1.0.tar.gz (source distribution)
# - dist/hot_spot_analysis-1.1.0-py3-none-any.whl (wheel)
```

Verify the build:

```bash
ls -lh dist/

# Should show:
# -rw-r--r-- 1 user user  XX KB hot_spot_analysis-1.1.0-py3-none-any.whl
# -rw-r--r-- 1 user user  XX KB hot_spot_analysis-1.1.0.tar.gz
```

#### 4. Test on TestPyPI (Recommended)

Upload to TestPyPI first to catch any issues:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps hot-spot-analysis==1.1.0

# Verify import works
python -c "from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer; print('✓ Import successful!')"

# Run a quick integration test
python -c "
from hot_spot_analysis.utils import demo
from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer

tips = demo.tips()
df_tips = tips.build_df(stack_count=2)
HSA = HotSpotAnalyzer(
    data=df_tips,
    target_cols=['day', 'smoker'],
    interaction_limit=1,
    objective_function=tips.calc_tip_stats,
)
HSA.run_hsa()
print('✓ Integration test passed!')
"

# Uninstall test version
pip uninstall hot-spot-analysis -y
```

#### 5. Publish to PyPI (Production)

Once TestPyPI testing is successful:

```bash
# Upload to production PyPI
python -m twine upload dist/*

# You'll see output like:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading hot_spot_analysis-1.1.0-py3-none-any.whl
# Uploading hot_spot_analysis-1.1.0.tar.gz
# View at: https://pypi.org/project/hot-spot-analysis/1.1.0/
```

#### 6. Verify Publication

```bash
# Wait ~30 seconds for PyPI to process, then install
pip install --upgrade hot-spot-analysis

# Verify version
python -c "import importlib.metadata; print('Installed version:', importlib.metadata.version('hot-spot-analysis'))"

# Should output: Installed version: 1.1.0
```

#### 7. Create Git Tag and GitHub Release

```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release version 1.1.0: Dictionary/JSON optimizations and performance improvements"

# Push tag to GitHub
git push origin v1.1.0

# Create GitHub release manually via web UI or using gh CLI:
# gh release create v1.1.0 \
#   --title "v1.1.0: Comprehensive Refactoring" \
#   --notes-file CHANGELOG.md \
#   dist/hot_spot_analysis-1.1.0.tar.gz \
#   dist/hot_spot_analysis-1.1.0-py3-none-any.whl
```

---

## Using Makefile (Recommended)

Create a `Makefile` in the project root for streamlined releases:

```makefile
.PHONY: clean build test-build test-release release help

help:
	@echo "Available commands:"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make test-build   - Build and check packages"
	@echo "  make test-release - Upload to TestPyPI"
	@echo "  make release      - Upload to PyPI and create git tag"

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build
	@echo "✓ Build complete. Files in dist/:"
	@ls -lh dist/

test-build: build
	python -m twine check dist/*
	@echo "✓ Package check passed"

test-release: test-build
	python -m twine upload --repository testpypi dist/*
	@echo "✓ Uploaded to TestPyPI"
	@echo "  Test install: pip install --index-url https://test.pypi.org/simple/ --no-deps hot-spot-analysis"

release: test-build
	@echo "Uploading to PyPI..."
	python -m twine upload dist/*
	@echo "✓ Uploaded to PyPI"
	@echo "Creating git tag v$(VERSION)..."
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin v$(VERSION)
	@echo "✓ Release complete!"

# Use like: make release VERSION=1.1.0
```

Then run:

```bash
make test-release VERSION=1.1.0  # Test first
make release VERSION=1.1.0       # Production release
```

---

## Troubleshooting

### Issue: "File already exists"

If you get an error about files already existing on PyPI:

```bash
# You cannot re-upload the same version. Increment version number:
# Edit pyproject.toml and change version to 1.1.1
# Then rebuild and upload
```

### Issue: Authentication Failed

```bash
# Generate a PyPI API token at https://pypi.org/manage/account/token/
# Use __token__ as username and the token (including pypi- prefix) as password
# Or configure ~/.pypirc as shown in prerequisites
```

### Issue: Package Validation Failed

```bash
# Check package before upload
python -m twine check dist/*

# Common issues:
# - Missing README.md
# - Invalid metadata in pyproject.toml
# - Missing required files
```

### Issue: Import Errors After Install

```bash
# Clear pip cache and reinstall
pip cache purge
pip uninstall hot-spot-analysis -y
pip install hot-spot-analysis==1.1.0
```

---

## Post-Release Checklist

- [ ] Package visible at https://pypi.org/project/hot-spot-analysis/1.1.0/
- [ ] Installation via `pip install hot-spot-analysis` works
- [ ] Version number correct: `python -c "import importlib.metadata; print(importlib.metadata.version('hot-spot-analysis'))"`
- [ ] Git tag pushed: `git tag -l v1.1.0`
- [ ] GitHub release created with release notes
- [ ] Update documentation if needed
- [ ] Announce release (if applicable)

---

## Version 1.1.0 Changes

### Improvements

1. **Direct Dictionary Creation** - Eliminated temporary column creation in `_process_hsa_raw_output_dicts()`
2. **List Comprehensions** - Replaced for-loop-append patterns across 4 files
3. **Performance** - Reduced memory overhead and improved execution speed
4. **Code Quality** - Removed ~28 lines of code while improving readability

### Deprecations

- `lists_to_dict()` - Deprecated in favor of list comprehension with `dict(zip())`
  - Migration: `[dict(zip(keys, values)) for keys, values in zip(keys_column, values_column)]`
  - Will be removed in version 2.0.0

### Backward Compatibility

✅ All public APIs unchanged
✅ Existing code continues to work
✅ No breaking changes

---

## Quick Reference

```bash
# Complete release in one go
rm -rf dist/ && python -m build && python -m twine upload dist/* && git tag -a v1.1.0 -m "Release 1.1.0" && git push origin v1.1.0
```
