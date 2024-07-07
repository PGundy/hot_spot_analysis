import os
import subprocess
from pathlib import Path

import pandas as pd

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


def get_repo_root():
    try:
        # Run the git command to get the top-level directory of the repository
        repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).strip().decode("utf-8")
        return Path(repo_root)
    except subprocess.CalledProcessError:
        raise RuntimeError("This is not a git repository.")


def build_demo_data_from_local_data(file_name="tips_dataset.csv", stack_count: int = 10):
    root_dir = get_repo_root()
    data_folder_dir = os.path.join(root_dir, "data")
    file_path = os.path.join(data_folder_dir, file_name)

    if os.path.exists(file_path):
        return data_stacker(pd.read_csv(file_path), stack_count)
    else:
        available_files = os.listdir(data_folder_dir)
        regex = "\n\t"
        raise FileNotFoundError(
            f"File '{file_name}' not found in {data_folder_dir}. Available files: {regex+regex.join(available_files)}"
        )


class tips:
    def build_df(self, stack_count=10) -> pd.DataFrame:
        df_tips = build_demo_data_from_local_data(stack_count=stack_count)
        df_tips["tip_perc"] = df_tips["tip"] / df_tips["total_bill"]
        return df_tips

    def calc_tip_stats(self, data: pd.DataFrame) -> pd.DataFrame:
        df_agg = data.agg(
            avg_tips=pd.NamedAgg("tip", "mean"),
            avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
        ).round(2)
        return df_agg
