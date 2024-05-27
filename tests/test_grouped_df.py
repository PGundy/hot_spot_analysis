# %%
import pandas as pd
import pytest

from hot_spot_analysis.utils import grouped_df


class TestDataFunctions:
    @staticmethod
    def test_is_grouped():
        # TODO: remove the need for this function, and just take groupby as arg in HSA
        # Define grouped DataFrame test data
        df_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}).groupby("A")

        # Test is_grouped with grouped DataFrame
        assert grouped_df.is_grouped(df_grouped) is True  # type: ignore

        # Define non-grouped DataFrame test data
        df_non_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        # Test is_grouped with non-grouped DataFrame
        assert grouped_df.is_grouped(df_non_grouped) is False

    @staticmethod
    def test_get_groups():
        # TODO: remove the need for this function, and just take groupby as arg in HSA
        # Define grouped DataFrame test data
        df_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}).groupby("A")

        # Test get_groups with grouped DataFrame
        assert grouped_df.get_groups(df_grouped) == ["A"]  # type: ignore

        # Define non-grouped DataFrame test data
        df_non_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        # Test get_groups with non-grouped DataFrame
        assert grouped_df.get_groups(df_non_grouped) == [None]

    @staticmethod
    def test_return_data():
        # TODO: remove the need for this function, and just take groupby as arg in HSA
        # Define grouped DataFrame test data
        df_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}).groupby("A")
        expected_output_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        # Test return_data with grouped DataFrame
        assert grouped_df.return_data(df_grouped).equals(expected_output_grouped)  # type: ignore

        # Define non-grouped DataFrame test data
        df_non_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        expected_output_non_grouped = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        # Test return_data with non-grouped DataFrame
        assert grouped_df.return_data(df_non_grouped).equals(expected_output_non_grouped)

    @staticmethod
    def test_add_groups_to_combos():
        # Define group_vars and combos test data
        group_vars = ["A"]
        combos = [["B"], ["C"]]
        expected_output = [["A", "B"], ["A", "C"]]

        # Test add_groups_to_combos function
        assert grouped_df.add_groups_to_combos(group_vars, combos) == expected_output


# Execute the tests
if __name__ == "__main__":
    pytest.main()
