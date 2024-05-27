import pytest

from hot_spot_analysis.utils import combos


# Unit test for create_combos function
def test_create_combos():
    # Test case 1: Test with interaction_max = 3
    target_cols = ["A", "B", "C"]
    expected_output = [
        ["A"],
        ["B"],
        ["C"],
        ["A", "B"],
        ["A", "C"],
        ["B", "C"],
        ["A", "B", "C"],
    ]
    assert combos.create_combos(target_cols) == expected_output, "Test case 1 failed"

    # Test case 2: Test with custom target_cols and interaction_max
    target_cols = ["X", "Y", "Z", "W"]
    interaction_max = 2
    expected_output = [
        ["X"],
        ["Y"],
        ["Z"],
        ["W"],
        ["X", "Y"],
        ["X", "Z"],
        ["X", "W"],
        ["Y", "Z"],
        ["Y", "W"],
        ["Z", "W"],
    ]
    assert combos.create_combos(target_cols, interaction_max) == expected_output, "Test case 2 failed"


# Execute the tests
if __name__ == "__main__":
    pytest.main()
