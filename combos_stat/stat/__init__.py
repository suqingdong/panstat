import math
import itertools
import pathlib
from typing import Iterable, Literal, Optional, Tuple, Union, Set, Dict

import tqdm
import pandas as pd

from combos_stat import util


class CombosStat(object):
    """
    A utility class to compute shared data statistics for given combinations of data samples.

    Attributes:
        input_file (Path): Path to the input data file.
        output_file (Path): Path where the results will be saved.
        num_samples (int): Number of samples to compute.
        share_type (str): Type of share to compute ('intersection' or 'union').
        header (int): Row number to use as the column names.
        sep (str): Delimiter to use for reading the input file.
        start_col (int): Column index to start reading sample data from.
        show_progress (bool): Flag to indicate if a progress bar should be displayed.
    """

    def __init__(self,
                 input_file: str,
                 num_samples: int,
                 share_type: Literal['intersection', 'union'],
                 header: Optional[int] = 0,
                 sep: str = '\t',
                 start_col: int = 1,
                 show_progress: Optional[bool] = True,
                 chunksize: Optional[int] = None,
                 chunk: Optional[int] = None,
                 **kwargs,
                 ):
        self.input_file = input_file
        self.num_samples = num_samples
        self.share_type = share_type
        self.header = header
        self.sep = sep
        self.start_col = start_col
        self.show_progress = show_progress
        self.chunksize = chunksize
        self.chunk = chunk

        self.combinations_length = None

    def load_data(self) -> Tuple[Dict[str, Set[int]], Iterable[Tuple], int]:
        """
        Load data from the input file and prepare sample combinations.

        Returns:
            Tuple containing:
                - data_sets (Dict[str, Set[int]]): Dictionary with sample names as keys and corresponding data sets as values.
                - sample_combinations (Iterable[Tuple]): Combinations of sample names.
        """
        self.sep = '\t' if self.sep == '\\t' else self.sep

        if self.chunk and self.chunksize:
            util.logger.info(f'load data from file: {self.input_file} [chunk: {self.chunk}, chunksize: {self.chunksize}]')
            chunks = pd.read_csv(self.input_file, header=self.header, sep=self.sep, chunksize=self.chunksize)
            df = next(itertools.islice(chunks, self.chunk - 1, None))
        else:
            util.logger.info(f'load data from file: {self.input_file}')
            df = pd.read_csv(self.input_file, header=self.header, sep=self.sep)

        samples = df.columns[self.start_col:]
        combinations = itertools.combinations(samples, self.num_samples)
        self.combinations_length = math.comb(len(samples), self.num_samples)

        # Compute the set of positions where data > 0 for each sample
        data_sets = {
            sample: set(df[df[sample] > 0].index) for sample in samples
        }

        return data_sets, combinations

    def count_shared(self, sample_sets: Iterable[Set[int]]) -> int:
        """
        Count the shared data for a given set of samples.

        Args:
            sample_sets (Iterable[Set[int]]): List of data sets for each sample in the combination.

        Returns:
            int: Number of shared data points.
        """
        if self.share_type == 'intersection':
            shared_set = set.intersection(*sample_sets)
        else:
            shared_set = set.union(*sample_sets)
        return len(shared_set)

    def process_combinations(self, data_sets: Dict[str, Set[int]], combinations: Iterable[Tuple]) -> Iterable[int]:
        """
        Process combinations of samples and compute shared data counts.

        Args:
            data_sets (Dict[str, Set[int]]): Dictionary with sample names as keys and corresponding data sets as values.
            combinations (Iterable[Tuple]): Combinations of sample names.

        Returns:
            Iterable[int]: Shared data counts for each combination.
        """
        for combination in combinations:
            sample_sets = [data_sets[sample] for sample in combination]
            yield self.count_shared(sample_sets)

    def compute(self) -> Iterable[int]:
        """
        Compute shared data counts for each combination of samples.

        This method processes combinations of samples from the input data and calculates 
        the shared data counts based on the specified share type (intersection or union). 
        The results are returned as an iterable of integers, where each integer represents 
        the shared data count for a specific combination.

        Returns:
            Iterable[int]: Shared data counts for each combination of samples.
        """
        data_sets, combinations = self.load_data()
        results = self.process_combinations(data_sets, combinations)
        return results

    def save(self, results: Iterable[int], output_file: str):
        """
        Save the computed results to a specified output file.

        Args:
            results (Iterable[int]): The computed shared data counts for each combination.
            output_file (str): The path to the output file where the results should be saved.
        """
        util.logger.debug('start saving result ...')

        if self.show_progress:
            results = tqdm.tqdm(results, desc='Processing combinations', unit='lines', total=self.combinations_length)

        output_path = pathlib.Path(output_file)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        buffer_size = 1000
        buffer = []
        with output_path.open('w') as f:
            for result in results:
                buffer.append(f'{result}\n')
                if len(buffer) >= buffer_size:
                    f.writelines(buffer)
                    buffer.clear()
            f.writelines(buffer)

        util.logger.info(f'saved to file: {output_path}')


if __name__ == '__main__':
    combos = CombosStat(input_file='tests/family.stat', num_samples=3, share_type='intersection')
    util.logger.debug('start normal mode')
    results = combos.compute()
    list(results)
    util.logger.debug('complete normal mode')

    combos = CombosStat(input_file='tests/family.stat', num_samples=3, share_type='intersection', chunksize=100, chunk=20)
    util.logger.debug('start chunk mode')
    results = combos.compute()
    list(results)
    util.logger.debug('complete chunk mode')
