from pathlib import Path

import pandas as pd


def stat_from_result(result_dir: str):
    result_dir = Path(result_dir)

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

    final_df.to_csv('processed_stats.tsv', sep='\t', index=False)