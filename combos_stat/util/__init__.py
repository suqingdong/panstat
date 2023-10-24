import math
from pathlib import Path
import textwrap
from typing import List, Dict

from simple_loggers import SimpleLogger


logger = SimpleLogger('CombosStat')


def dynamic_chunkcount(sample_count: int, threshold: int = 50000) -> Dict[int, int]:
    """
    Calculate the dynamic chunk size for each group size based on a threshold.

    """
    num_samples = list(range(2, sample_count + 1))
    combinations = [math.comb(sample_count, i) for i in num_samples]

    chunkcounts = [comb // threshold or 1 for comb in combinations]

    return dict(zip(num_samples, chunkcounts))


def generate_stat_shell(chunkcounts: Dict[int, int],
                   total_lines: int,
                   input_file: str,
                   shell_dir: Path,
                   result_dir: Path,
                   start_col: int,
                   sep: str):
    """
    Generate shell scripts for statistical analysis based on input parameters.

    This function produces shell scripts that will execute the `combos_stat` command with specific
    parameters, including input file, output file, column starting position, separator, number of samples,
    share type, chunk size, and chunk number. The generated scripts will be placed in specified directories.

    Parameters:
    - chunkcounts (Dict[int, int]): A dictionary mapping the number of samples to the number of chunks.
    - total_lines (int): Total number of lines in the input file.
    - input_file (str): Path to the input data file.
    - shell_dir (Path): Directory where the generated shell scripts will be saved.
    - result_dir (Path): Directory where the result files will be saved.
    - start_col (int): Column number to start the statistical analysis.
    - sep (str): Separator used in the input file.

    Yields:
    - Path: Path to the generated shell script.
    """

    if sep == '\t':
        sep = r'\\t'

    logger.debug(f'{input_file} total_lines: {total_lines}')

    for num_samples, chunkcount in chunkcounts.items():
        chunksize = math.ceil(total_lines / chunkcount) if chunkcount > 1 else 0
        logger.debug(f'>>> num_samples: {num_samples}: chunkcount: {chunkcount}, chunksize: {chunksize}')

        for chunk in range(1, chunkcount + 1):
            for prefix, share_type in zip('xy', ('union', 'intersection')):
                stat_shell = shell_dir / f'{prefix}{num_samples}' / f'stat.{prefix}{num_samples}_{chunk}.sh'
                output_file = result_dir / f'{prefix}{num_samples}' / f'{prefix}{num_samples}_{chunk}.txt'
                stat_shell.parent.mkdir(parents=True, exist_ok=True)
                cmd = textwrap.dedent(f'''\
                    combos_stat stat \\
                        -i {Path(input_file).resolve()} \\
                        -o {output_file} \\
                        --start-col {start_col} \\
                        --sep {sep} \\
                        -n {num_samples} \\
                        -t {share_type} \\
                        --chunksize {chunksize} \\
                        --chunk {chunk}
                ''')
                stat_shell.write_text(cmd)
                yield stat_shell


def generate_plot_shell(result_dir: Path, shell_dir: Path):
    """
    Generate a shell script for plotting results using the `combos_stat` command.

    This function creates a shell script that will execute the `combos_stat plot` command 
    with the specified result directory. The generated script will be saved in the provided shell directory.

    Parameters:
    - result_dir (Path): Directory containing the result files to be plotted.
    - shell_dir (Path): Directory where the generated shell script will be saved.

    Returns:
    - Path: Path to the generated shell script.
    """

    plot_shell = shell_dir / 'plot.sh'
    cmd = f'combos_stat plot {result_dir}'
    plot_shell.write_text(cmd)
    return plot_shell