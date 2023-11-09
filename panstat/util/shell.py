import math
from pathlib import Path
import textwrap
from typing import Literal, Dict

from . import logger


def generate_stat_shell(chunkcounts: Dict[int, int],
                        total_lines: int,
                        input_file: str,
                        shell_dir: Path,
                        result_dir: Path,
                        start_col: int,
                        sep: str):
    """
    Generate shell scripts for statistical analysis based on input parameters.

    This function produces shell scripts that will execute the `panstat` command with specific
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
            for prefix, share_type in zip('xy', ('intersection', 'union')):
                stat_shell = shell_dir / f'{prefix}{num_samples}' / f'stat.{prefix}{num_samples}_{chunk}.sh'
                output_file = result_dir / f'{prefix}{num_samples}' / f'{prefix}{num_samples}_{chunk}.txt'
                stat_shell.parent.mkdir(parents=True, exist_ok=True)
                cmd = textwrap.dedent(f'''\
                    panstat stat \\
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


def generate_merge_shell(result_dir: Path, shell_dir: Path, merge_dir: str = 'merge'):
    """
    Generate a shell to merge the results.

    Args:
        result_dir: The directory where the results are stored.
        shell_dir: The directory where the shell will be stored.
        merge_dir: The merged result directory

    Returns:
        A Path object to the shell.
    """
    merge_shell = shell_dir / 'merge.sh'
    cmd = f'panstat merge {result_dir} -o {merge_dir}\n'
    merge_shell.write_text(cmd)
    return merge_shell


def generate_plot_shell(result_dir: Path,
                        shell_dir: Path,
                        plot_type: Literal['point', 'box'] = 'point',
                        processed_file: str = Path('processed_stats.tsv').resolve(),
                        output_dir: Path = Path('.').resolve()):
    """
    Generate a shell to plot the results.

    Args:
        result_dir: The directory where the results are stored.
        shell_dir: The directory where the shell will be stored.
        plot_type: The type of plot to generate.
        processed_file: The processed file.

    Returns:
        A Path object to the shell.
    """
    plot_shell = shell_dir / 'plot.sh'
    r_script = output_dir / f'{plot_type}_plot.R'
    outfile = output_dir / f'{plot_type}plot'
    cmd = textwrap.dedent(f'''
        panstat plot {result_dir} \\
            --write {r_script} \\
            --plot-type {plot_type} \\
            --option infile={processed_file} \\
            --option output={outfile}
    ''')
    plot_shell.write_text(cmd)
    return plot_shell
