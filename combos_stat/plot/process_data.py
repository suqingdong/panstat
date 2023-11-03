from typing import Literal
from pathlib import Path

import pandas as pd

from combos_stat import util


def stat_from_result(result_dir: str, outfile: str = 'processed_stats.tsv', plot_type: Literal['point', 'box'] = 'points'):
    """
    Process and aggregate statistics from result files located in the specified directory.

    This function reads individual text files from subdirectories (starting with 'x' or 'y')
    in the given result directory, aggregates the data, and computes descriptive statistics 
    (mean, min, percentiles, max). The aggregated statistics are then written to a TSV outfile.

    Parameters:
    - result_dir (str): The path to the directory containing the result subdirectories and files.
    - outfile (str, optional): The name of the output file to which the aggregated statistics will be written.
                               Default is 'processed_stats.tsv'.
    - plot_type (str, optional): The type of plot to use for the aggregated statistics.

    Returns:
    - str: The name of the output file with aggregated statistics.

    Note:
    The function expects the result directory to contain subdirectories starting with 'x' or 'y',
    and each subdirectory should contain '.txt' files with the data.
    """

    result_dir = Path(result_dir)

    util.logger.debug(f'stat from result dir: {result_dir}')

    if plot_type == 'point':
        columns = 'share_count share_type value'.split()
    else:
        columns = 'share_count share_type mean min p25 p50 p75 max'.split()

    with open(outfile, 'w') as out:
        out.write('\t'.join(columns) + '\n')

        for p in (result_dir.glob('[xy]*')):
            share_type = p.name[0]
            share_type = 'core' if share_type == 'x' else 'pan'
            share_count = p.name[1:]

            sum_df = None
            for file in p.glob('*.txt'):
                util.logger.debug(f'stat from file: {file}')
                df = pd.read_csv(file, header=None, names=['x']).x
                if sum_df is None:
                    sum_df = df
                else:
                    sum_df += df

            print(sum_df.size)

            if plot_type == 'point':
                representative_values = util.get_representative_values(sum_df)
                for value in representative_values:
                    out.write(f'{share_count}\t{share_type}\t{value}\n')
            else:
                df_stats = sum_df.describe()
                lines = [share_count, share_type] + df_stats.loc[['mean', 'min', '25%', '50%', '75%', 'max']].to_list()
                out.write('\t'.join(map(str, lines)) + '\n')

    util.logger.debug(f'saved aggregated statistics to {outfile}')

    return outfile
