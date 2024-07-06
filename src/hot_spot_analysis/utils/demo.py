import pandas as pd
import seaborn as sns

"""

Some functions to make demo-ing HotSpotAnalyzer easier

"""


def data_stacker(df: pd.DataFrame, stack_count: int = 10) -> pd.DataFrame:
    """Stacks the given DataFrame vertically multiple times.

    Args:
        df (pd.DataFrame): Input DataFrame to stack.
        stack_count (int, optional): Number of times to stack the DataFrame. Defaults to 10.

    Returns:
        pd.DataFrame: Stacked DataFrame.
    """
    df_stacks = []

    for i in range(1, stack_count + 1):
        # Repeat the DataFrame 'i' times and reset index
        df_temp = pd.concat([df] * i).reset_index(drop=True)

        # Add a 'timestamp' column with scalar values
        df_temp["fake_ts"] = i

        # Append the stacked DataFrame to the list
        df_stacks.append(df_temp)

    # Concatenate all stacked DataFrames into one
    df_stacked = pd.concat(df_stacks)

    return df_stacked


def build_demo_df_from_sns_datasets(sns_dataset="tips", stack_count: int = 10):
    df_demo = data_stacker(
        df=sns.load_dataset(sns_dataset),
        stack_count=stack_count,
    )
    return df_demo
