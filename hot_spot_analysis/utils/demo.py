import numpy as np
import pandas as pd


def data_stacker(df: pd.DataFrame, stack_count: int = 10):
    stacks = np.arange(stack_count)
    df_stacks = []
    for i, _ in enumerate(stacks):
        scalar = i + 1
        df_temp = pd.concat([df] * scalar).reset_index(drop=True)
        df_temp["timestamp"] = pd.Series([scalar] * len(df_temp))
        df_stacks.append(df_temp)

    df_stacked: pd.DataFrame = pd.concat(df_stacks)
    return df_stacked
