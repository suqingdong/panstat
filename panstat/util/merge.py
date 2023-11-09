from pathlib import Path
from functools import partial
from multiprocessing import Pool

import numpy as np

from . import logger


def merge_path_result(merge_dir: str, path: Path):

    logger.debug(f'merge result for: {path.name}')

    out_path = Path(merge_dir) / path.name / f'{path.name}.txt'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sum_data = None
    for file in path.glob('*.txt'):
        logger.debug(f'read file: {file.name}')
        data = np.loadtxt(file, dtype=np.int64)
        if sum_data is None:
            sum_data = data
        else:
            sum_data += data

    np.savetxt(out_path, sum_data.reshape(-1), fmt='%d')

    logger.debug(f'saved merged results to {out_path}')


def merge_result(result_dir: str, merge_dir: str = 'merge'):
    result_dir = Path(result_dir)

    logger.debug(f'stat from result dir: {result_dir}')

    result_paths = list(result_dir.glob('[xy]*'))
    logger.debug(f'found {len(result_paths)} result paths: {result_paths}')
    
    with Pool() as pool:
        pool.map(partial(merge_path_result, merge_dir), result_paths)
