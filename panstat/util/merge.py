from pathlib import Path

import pandas as pd

from . import logger


def merge_result(result_dir: str, merge_dir: str = 'merge'):
    result_dir = Path(result_dir)

    logger.debug(f'stat from result dir: {result_dir}')

    for p in (result_dir.glob('[xy]*')):

        out_path = Path(merge_dir) / p.name / f'{p.name}.txt'
        out_path.parent.mkdir(parents=True, exist_ok=True)

        sum_df = None
        for file in p.glob('*.txt'):

            logger.debug(f'stat from file: {file}')
            df = pd.read_csv(file, header=None, names=['x']).x
            if sum_df is None:
                sum_df = df
            else:
                sum_df += df

        sum_df.to_csv(out_path, header=False, index=False)
        logger.debug(f'saved merged results to {out_path}')
