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
                    python3 -m combos_stat.bin.main stat \\
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
    plot_shell = shell_dir / 'plot.sh'
    cmd = f'python3 -m combos_stat.bin.main plot {result_dir}'
    plot_shell.write_text(cmd)
    return plot_shell