# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-09

### Added
- Comprehensive RELEASE.md documentation with detailed PyPI publishing instructions
- CHANGELOG.md to track version history
- Deprecation warning for `lists_to_dict()` function with migration guidance

### Changed
- **BREAKING (Minor)**: `lists_to_dict()` is now deprecated (will be removed in 2.0.0)
  - Use list comprehension instead: `[dict(zip(keys, values)) for keys, values in zip(keys_column, values_column)]`
- Optimized `_process_hsa_raw_output_dicts()` to create dictionaries directly without temporary columns
  - Before: Created `combo_keys` and `combo_values` columns, then zipped and dropped them (14 lines)
  - After: Single operation with `dict(zip())` (3 lines)
  - **Impact**: 11 lines removed, eliminated temporary column overhead
- Refactored `_pop_key_off_combo_dict()` to use list comprehension instead of for-loop
  - Reduced from 5 lines to 3 lines
- Optimized `search_hsa_output()` list comprehension combination
  - Removed unnecessary `search_vector = []` initialization
  - Combined two-step list comprehension into single operation with `any()`
  - Eliminated intermediate list creation for better performance

### Improved
- **utils/grouped_df.py**: Refactored `add_groups_to_combos()` to single-line list comprehension
  - Reduced from 5 lines to 1 line
- **utils/demo.py**: Refactored `data_stacker()` to use list comprehension with pandas `.assign()`
  - Reduced from 13 lines to 5 lines
  - More readable and Pythonic
- **Code Quality**: Removed ~28 lines of code overall while improving readability
- **Performance**: Reduced memory overhead through elimination of temporary data structures
- **Consistency**: Uniform use of list comprehensions across entire codebase

### Fixed
- N/A

### Deprecated
- `lists_to_dict()` in utils/lists.py (deprecated in 1.1.0, will be removed in 2.0.0)

### Removed
- N/A

### Security
- N/A

### Testing
- All 14 unit tests pass
- Integration tests verify end-to-end functionality
- Deprecation warnings work correctly

### Migration Guide

If you're using `lists_to_dict()` directly in your code:

**Before (deprecated):**
```python
from hot_spot_analysis.utils import lists

result = lists.lists_to_dict(
    keys_column=[["a", "b"], ["c", "d"]],
    values_column=[[1, 2], [3, 4]]
)
```

**After (recommended):**
```python
keys_column = [["a", "b"], ["c", "d"]]
values_column = [[1, 2], [3, 4]]

result = [
    dict(zip(keys, values))
    for keys, values in zip(keys_column, values_column)
]
```

---

## [1.0.4.1] - Previous Release

### Summary
- Initial stable release with core Hot Spot Analysis functionality
- Support for multi-dimensional data analysis
- Grouping and time-period analysis capabilities
- Comprehensive test suite

---

## Release Statistics

### Version 1.1.0
- **Files Modified**: 4
- **Lines Added**: 29
- **Lines Removed**: 57
- **Net Change**: -28 lines
- **Functions Optimized**: 5
- **Performance Improvement**: Reduced memory overhead, faster list operations
- **Breaking Changes**: 0 (fully backward compatible)
- **Deprecations**: 1 (lists_to_dict)

### Compatibility
- **Python**: >=3.9 (unchanged)
- **pandas**: >=1.3.5 (unchanged)
- **numpy**: >=1.21 (unchanged)
- **Backward Compatible**: Yes ✅
- **API Changes**: None (only deprecation warnings)

---

## Links

- [PyPI Package](https://pypi.org/project/hot-spot-analysis/)
- [GitHub Repository](https://github.com/pgundy/hot_spot_analysis)
- [Issue Tracker](https://github.com/pgundy/hot_spot_analysis/issues)

---

[1.1.0]: https://github.com/pgundy/hot_spot_analysis/compare/v1.0.4.1...v1.1.0
[1.0.4.1]: https://github.com/pgundy/hot_spot_analysis/releases/tag/v1.0.4.1
