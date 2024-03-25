"""
functions that handle the combinations to reduce code complexity elsewhere
"""
import itertools

import numpy as np


def create_combos(target_cols: list[str], interaction_max: int = 3):
    """Build the combinations of target_cols for 0->interaction_max

    Args:
        target_cols (list[str]): _description_
        interaction_max (int, optional): limits interactions. Defaults to 3.

    Returns:
        list[str]: target_cols for combination lengths 0->interaction_max
    """
    combos_nested = []  # 1 layer more nested than combos_final
    combos_final: list[list[str]] = []

    def combo_interaction_i(interactions: int):
        """
        Build combos with 1->X interactions
        """
        combo_interim = []
        for combo in itertools.combinations(target_cols, interactions):
            combo_interim.append(list(combo))
        return combo_interim

    for interaction_i in np.arange(interaction_max) + 1:
        # Build combinations up through the interaction max
        combos = combo_interaction_i(interaction_i)
        combos_nested.append(combos)

    # Now convert the

    combos_final = list(itertools.chain.from_iterable(combos_nested))
    return combos_final
