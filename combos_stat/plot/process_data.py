from pathlib import Path

import pandas as pd

from combos_stat import util


def stat_from_result(result_dir: str, outfile: str = 'processed_stats.tsv'):
    """
    Process and aggregate statistics from result files located in the specified directory.

    This function reads individual text files from subdirectories (starting with 'x' or 'y')
    in the given result directory, aggregates the data, and computes descriptive statistics 
    (mean, min, percentiles, max). The aggregated statistics are then written to a TSV outfile.

    Parameters:
    - result_dir (str): The path to the directory containing the result subdirectories and files.
    - outfile (str, optional): The name of the output file to which the aggregated statistics will be written.
                               Default is 'processed_stats.tsv'.

    Returns:
    - str: The name of the output file with aggregated statistics.

    Note:
    The function expects the result directory to contain subdirectories starting with 'x' or 'y',
    and each subdirectory should contain '.txt' files with the data.
    """

    result_dir = Path(result_dir)

    util.logger.debug(f'stat from result dir: {result_dir}')

    columns = 'share_count share_type mean min p25 p50 p75 max'.split()
    final_df = pd.DataFrame(columns=columns)

    for p in (result_dir.glob('[xy]*')):
        share_type = p.name[0]
        share_type = 'core' if share_type == 'x' else 'span'
        share_count = p.name[1:]

        sum_df = None
        for file in p.glob('*.txt'):
            df = pd.read_csv(file, header=None)
            if sum_df is None:
                sum_df = df
            else:
                sum_df += df

        df_stats = sum_df.describe()[0]
        lines = [share_count, share_type] + df_stats.loc[['mean', 'min', '25%', '50%', '75%', 'max']].to_list()

        final_df = pd.concat([final_df, pd.DataFrame([lines], columns=columns)])

    final_df.to_csv(outfile, sep='\t', index=False)

    return outfile