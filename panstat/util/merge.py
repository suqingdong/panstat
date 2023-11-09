from pathlib import Path
from multiprocess import Pool

import numpy as np

from . import logger


def merge_result(result_dir: str, merge_dir: str = 'merge'):
    result_dir = Path(result_dir)

    logger.debug(f'stat from result dir: {result_dir}')

    for p in (result_dir.glob('[xy]*')):
        logger.debug(f'merge result for: {p.name}')

        out_path = Path(merge_dir) / p.name / f'{p.name}.txt'
        out_path.parent.mkdir(parents=True, exist_ok=True)

        sum_data = None
        for file in p.glob('*.txt'):
            logger.debug(f'read file: {file.name}')
            data = np.loadtxt(file, dtype=np.int64)
            if sum_data is None:
                sum_data = data
            else:
                sum_data += data

        with out_path.open('w') as out:
            for line in sum_data:
                out.write(f'{line}\n')

        logger.debug(f'saved merged results to {out_path}')
