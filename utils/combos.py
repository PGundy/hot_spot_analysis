import itertools

import numpy as np

from utils import list_funcs


# get the list of alphanumerically sorted combinations
def _create_combos(
    data_cuts: str, depth_limit: int = 3  ## rename to interaction_max
):
    """
    Creates the interaction combinations using the data_cuts input
    with an interaction maximum governed by depth_limit.

    Example:
        data_cuts = ['a','b','c']
        depth_limit = 2
        combinations: ['a','b','c', 'ab', 'bc']

    Returns a list(str)
    """

    if None in data_cuts:
        raise ValueError("\n\t\t" + "Invalid item in data_cuts: None")

    data_cuts = list_funcs._make_list_unique(data_cuts)

    data_cuts.sort()

    # define the interim objects
    combination_final = []
    for i in np.arange(1, depth_limit + 1, 1):
        combinations = list(itertools.combinations(data_cuts, int(i)))
        combinations = list(map(list, combinations))
        combinations.sort()

        # Build up nested list of all combinations
        combination_final = [*combination_final, combinations]

        if i == depth_limit:
            # unnest the combinations
            combination_final = list(
                itertools.chain.from_iterable(combination_final)
            )

    return combination_final
