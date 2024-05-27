import itertools
from typing import List


def create_combos(target_cols: List[str], interaction_max: int = 3) -> List[List[str]]:
    """Build combinations of target_cols for interactions from 0 to interaction_max.

    Args:
        target_cols (List[str]): List of column names to combine.
        interaction_max (int, optional): Maximum number of interactions. Defaults to 3.

    Returns:
        List[List[str]]: List of combinations of target_cols for interaction lengths from 0 to interaction_max.
    """
    combos_final: List[List[str]] = []

    # Helper function to generate combinations with a specified number of interactions
    def generate_combinations(interactions: int) -> List[List[str]]:
        return [list(combo) for combo in itertools.combinations(target_cols, interactions)]

    # Generate combinations for each interaction level up to interaction_max
    for interaction_i in range(1, interaction_max + 1):
        combos_final.extend(generate_combinations(interaction_i))

    return combos_final
