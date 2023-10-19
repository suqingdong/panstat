import math
import itertools
import pathlib
from typing import Iterable, Literal, Optional, Tuple, Set, Dict

import tqdm
import pandas as pd
from simple_loggers import SimpleLogger


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
        logger (SimpleLogger): Logger instance for logging messages.
    """

    def __init__(self,
                 input_file: str,
                 output_file: str,
                 num_samples: int,
                 share_type: Literal['intersection', 'union'],
                 header: Optional[int] = 0,
                 sep: str = '\t',
                 start_col: int = 1,
                 show_progress: Optional[bool] = True,
                 ):
        self.input_file = input_file
        self.output_file = pathlib.Path(output_file)
        self.num_samples = num_samples
        self.share_type = share_type
        self.header = header
        self.sep = sep
        self.start_col = start_col
        self.show_progress = show_progress
        self.logger = SimpleLogger('CombosStat')

    def load_data(self) -> Tuple[Dict[str, Set[int]], Iterable[Tuple], int]:
        """
        Load data from the input file and prepare sample combinations.

        Returns:
            Tuple containing:
                - data_sets (Dict[str, Set[int]]): Dictionary with sample names as keys and corresponding data sets as values.
                - sample_combinations (Iterable[Tuple]): Combinations of sample names.
                - total_combinations (int): Total number of sample combinations.
        """
        self.logger.info(f'load data from file: {self.input_file}')

        df = pd.read_csv(self.input_file, header=self.header, sep=self.sep)
        samples = df.columns[self.start_col:]
        combinations = itertools.combinations(samples, self.num_samples)
        combinations_length = math.comb(len(samples), self.num_samples)

        # Compute the set of positions where data > 0 for each sample
        data_sets = {
            sample: set(df[df[sample] > 0].index) for sample in samples
        }

        return data_sets, combinations, combinations_length

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

    def write_output(self, results, combinations_length):
        """
        Write the shared data counts to the output file. Optionally display a progress bar.

        Args:
            results (Iterable[int]): Shared data counts for each combination.
            total_combinations (int): Total number of sample combinations.
        """
        self.logger.debug('Writing results...')

        if self.show_progress:
            results = tqdm.tqdm(results, desc='Processing combinations',
                                unit='lines', total=combinations_length)

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        buffer_size = 1000
        buffer = []
        with self.output_file.open('w') as f:
            for result in results:
                buffer.append(f'{result}\n')
                if len(buffer) >= buffer_size:
                    f.writelines(buffer)
                    buffer.clear()
            f.writelines(buffer)

        self.logger.info(f'Results saved to: {self.output_file}')

    def execute(self):
        """
        Main execution method to load data, process combinations, and save results to the output file.
        """
        data_sets, combinations, combinations_length = self.load_data()
        results = self.process_combinations(data_sets, combinations)
        self.write_output(results, combinations_length)


if __name__ == '__main__':
    CombosStat(
        input_file='tests/demo.stat',
        output_file='out.txt',
        num_samples=3,
        share_type='union',
        show_progress=True,
    ).execute()
