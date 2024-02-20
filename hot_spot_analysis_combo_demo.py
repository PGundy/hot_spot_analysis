# %%
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

from utils2 import combos, lists

# %%

letters = [
    "a",  # 01
    "b",  # 02
    "c",  # 03
    "d",  # 04
    "e",  # 05
    "f",  # 06
    "g",  # 07
    "h",  # 08
    "i",  # 09
    "j",  # 10
    "k",  # 11
    "l",  # 12
    "m",  # 13
    "n",  # 14
    "o",  # 15
]

possible_interactions = np.arange(10) + 1

output_dicts = []
for interactions in possible_interactions:
    for i, _ in enumerate(letters):
        # if i == 0:
        #    next

        target_cols = letters[0:i]
        combinations = combos.create_combos(
            target_cols=target_cols,
            interaction_max=interactions,
        )

        output_dict = {
            "interactions": interactions,
            "count_target_cols": len(target_cols),
            "count_combinations": len(combinations),
            "count_combinations_log": np.log(len(combinations)),
            "target_cols": target_cols,
            "combinations": combinations,
        }
        output_dicts.append(output_dict)

df = pd.DataFrame().from_dict(output_dicts)
df.info()

# %%

df_viz = df.copy()
# df_viz["interactions"] = [str(x) for x in df_viz["interactions"]]
px.scatter(
    data_frame=df_viz,
    x="count_target_cols",
    y="interactions",
    color="interactions",
    size="count_combinations",
)

# %%
px.line(
    data_frame=df_viz,
    x="count_target_cols",
    y="count_combinations",
    log_y=True,
    color="interactions",
    # size="count_combinations",
)
# %%

px.line(
    data_frame=df_viz[df.count_target_cols >= df.interactions],
    x="interactions",
    y="count_combinations",
    # log_x=True,
    color="count_target_cols",
    # size="count_combinations",
)

# %%
