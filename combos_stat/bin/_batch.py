import os
import pathlib

import click
import pandas as pd

from combos_stat import util


@click.command(
    name='batch',
    no_args_is_help=True,
    help=click.style('Generate batch shells for given data', italic=True, fg='blue'),
)
@click.option('-i', '--input-file', help='Path to the input data file', type=click.Path(exists=True))
@click.option('-sep', '--sep', help='Delimiter to use for reading the input file (e.g., "\\t" for tab)', default='\t')
@click.option('-s', '--start-col', help='Column index to start reading sample data from', default=1, show_default=True, type=int)
@click.option('-t', '--threshold', help='The threshold to divide the combinations', type=int, default=200000, show_default=True)
@click.option('-O', '--output-dir', help='Path to the output directory', type=click.Path(), default='.', show_default=True)
@click.option('--job', help='Generate SJM Job', is_flag=True)
def main(**kwargs):

    input_file = kwargs['input_file']
    start_col = kwargs['start_col']
    sep = kwargs['sep']

    header = next(pd.read_csv(input_file, sep=sep, chunksize=1))
    sample_count = header.columns[start_col:].size

    chunkcounts = util.dynamic_chunkcount(sample_count, threshold=kwargs['threshold'])

    total_lines = pd.read_csv(input_file).size

    output_dir = pathlib.Path(kwargs['output_dir'])

    makejob_conf = pathlib.Path('makejob.conf')

    with makejob_conf.open('w') as conf:

        for shell in util.generate_shell(chunkcounts, total_lines, input_file, output_dir, start_col, sep):
            conf.write(f'{shell} 1G\n')
        cmd = f'makejob {makejob_conf} -o main.job'
        print(cmd)
        assert not os.system(cmd)


if __name__ == '__main__':
    main()
