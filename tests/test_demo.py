import numpy as np
import pandas as pd
import pytest

from hot_spot_analysis.utils import demo


def test_data_stacker():
    # Test with stack_count = 5
    df = pd.DataFrame({"A": [1, 2, 3]})
    expected_rows = sum(range(1, 6)) * len(df)
    stacked_df = demo.data_stacker(df, stack_count=5)
    assert len(stacked_df) == expected_rows, "Test case failed for stack_count = 5"

    # Test with a custom DataFrame
    df = pd.DataFrame({"X": ["a", "b"], "Y": [1, 2]})
    expected_columns = ["X", "Y", "fake_ts"]
    stacked_df = demo.data_stacker(df)
    print(stacked_df.columns.tolist())
    print(expected_columns)
    assert stacked_df.columns.tolist() == expected_columns, "Test case failed for custom DataFrame"


# Execute the tests
if __name__ == "__main__":
    pytest.main()
