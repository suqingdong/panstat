import math
import pathlib
import textwrap
from typing import List, Dict


def dynamic_chunkcount(sample_count: int, threshold: int = 50000) -> Dict[int, int]:
    """
    Calculate the dynamic chunk size for each group size based on a threshold.

    """
    if threshold < 1000:
        threshold = 1000
        print(f'WARNING: The threshold for dynamic chunking is set to {threshold}')

    num_samples = list(range(2, sample_count + 1))
    combinations = [math.comb(sample_count, i) for i in num_samples]

    chunkcounts = [comb // threshold or 1 for comb in combinations]

    return dict(zip(num_samples, chunkcounts))




def generate_shell(chunkcounts, total_lines, input_file, output_dir, start_col, sep):
    if sep == '\t':
        sep = r'\\t'

    for num_samples, chunkcount in chunkcounts.items():
        chunksize = math.ceil(total_lines / chunkcount) if chunkcount > 1 else 0

        for chunk in range(1, chunkcount + 1):
            # print(f'num_samples: {num_samples}: chunk: {chunk}, chunksize: {chunksize}')
            for prefix, share_type in zip('xy', ('union', 'intersection')):
                output_shell = output_dir / 'shell' / f'{prefix}{num_samples}' / f'stat.{prefix}{num_samples}_{chunk}.sh'
                output_file = output_dir / 'result' / f'{prefix}{num_samples}' / f'{chunk}.txt'
                output_shell.parent.mkdir(parents=True, exist_ok=True)
                cmd = textwrap.dedent(f'''\
                    python3 -m combos_stat.bin.main stat \\
                        -i {pathlib.Path(input_file).resolve()} \\
                        -o {output_file.resolve()} \\
                        --start-col {start_col} \\
                        --sep {sep} \\
                        -n {num_samples} \\
                        -t {share_type} \\
                        --chunksize {chunksize} \\
                        --chunk {chunk}
                ''')
                output_shell.write_text(cmd)
                yield output_shell





if __name__ == '__main__':
    print(dynamic_chunkcount(29, threshold=10000))
    print(dynamic_chunkcount(29, threshold=50000))
    print(dynamic_chunkcount(29, threshold=100000))
    print(dynamic_chunkcount(29, threshold=500000))