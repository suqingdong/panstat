import math
from pathlib import Path
import textwrap
from typing import Literal, Dict

import pandas as pd
import numpy as np
from simple_loggers import SimpleLogger


logger = SimpleLogger('PanStat')


def dynamic_chunkcount(sample_count: int, threshold: int = 50000) -> Dict[int, int]:
    """
    Calculate the dynamic chunk size for each group size based on a threshold.

    """
    num_samples = list(range(2, sample_count + 1))
    combinations = [math.comb(sample_count, i) for i in num_samples]

    chunkcounts = [math.ceil(comb / threshold) for comb in combinations]

    return dict(zip(num_samples, chunkcounts))


def get_representative_values(df: pd.DataFrame, num_splits: int=30):
    """
    This function takes a pandas DataFrame and an optional number of splits (default is 30) as input. It calculates the representative values for the given DataFrame by splitting the data into the specified number of parts, taking the mean of each part, and finding the minimum and maximum values. The representative values are returned as a list.

    Args:
        df (pd.DataFrame): The input DataFrame.
        num_splits (int, optional): The number of splits to use for calculating representative values. Default is 30.

    Returns:
        list: A list of representative values.
    """

    if df.size <= num_splits:
        return df.tolist()

    # Record the original minimum and maximum values
    min_value = df.min()
    max_value = df.max()

    sorted_data = df.sort_values()

    # Split the data into the specified number of parts
    splits = np.array_split(sorted_data, num_splits)

    # Calculate the representative values (mean)
    representative_values = [min_value] + [int(split.mean()) for split in splits[1:-1]] + [max_value]

    return representative_values