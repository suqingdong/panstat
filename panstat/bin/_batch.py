import os
from pathlib import Path

import click
import pandas as pd

from panstat import util
from panstat.util import shell


__epilog__ = click.style('''\n
\b
examples:
    panstat batch -h
    panstat batch -i input.txt -t 200000 -O out
    panstat batch -i input.txt -t 200000 --job run.job
    panstat batch -i input.txt -t 200000 --job run.job --point-type box
    panstat batch -i input.txt -t 200000 --job run.job --no-check
''', fg='green')


@click.command(
    name='batch',
    no_args_is_help=True,
    help=click.style('Generate batch shells and SJM job', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.option('-i', '--input-file', help='Path to the input data file', type=click.Path(exists=True))
@click.option('-sep', '--sep', help='Delimiter to use for reading the input file (e.g., "\\t" for tab)', default='\t')
@click.option('-s', '--start-col', help='Column index to start reading sample data from', default=1, show_default=True, type=int)
@click.option('-t', '--threshold', help='The threshold to divide the combinations', type=int, default=200000, show_default=True)
@click.option('-O', '--output-dir', help='Path to the output directory', type=click.Path(), default='.', show_default=True)
@click.option('--merge-dir', help='Path to the merge directory', type=click.Path(), default='merge', show_default=True)
@click.option('-T', '--plot-type', help='The type of plot', type=click.Choice(['point', 'box']), default='point', show_default=True,
              show_choices=True)
@click.option('--job', help='Generate SJM Job')
@click.option('--no-check', help='Do not check queues for SJM', is_flag=True)
def main(**kwargs):

    input_file = kwargs['input_file']
    start_col = kwargs['start_col']
    plot_type = kwargs['plot_type']
    sep = kwargs['sep']
    job = kwargs['job']

    header = next(pd.read_csv(input_file, sep=sep, chunksize=1))
    sample_count = header.columns[start_col:].size

    util.logger.debug(f'>>> Found {sample_count} samples in {input_file}')

    chunkcounts = util.dynamic_chunkcount(sample_count, threshold=kwargs['threshold'])

    total_lines = pd.read_csv(input_file).size

    output_dir = Path(kwargs['output_dir']).resolve()
    merge_dir = Path(kwargs['merge_dir']).resolve()

    shell_dir = output_dir / 'shell'
    result_dir = output_dir / 'result'

    makejob_conf = Path('makejob.conf')

    with makejob_conf.open('w') as conf:
        stat_shells = None
        for stat_shell in shell.generate_stat_shell(chunkcounts=chunkcounts,
                                                    total_lines=total_lines,
                                                    input_file=input_file,
                                                    shell_dir=shell_dir,
                                                    result_dir=result_dir,
                                                    start_col=start_col,
                                                    sep=sep):
            conf.write(f'{stat_shell} 1G\n')
            if stat_shells is None:
                stat_shells = str(stat_shell)
            else:
                stat_shells += f',{stat_shell}'

        merge_shell = shell.generate_merge_shell(result_dir=result_dir,
                                                 shell_dir=shell_dir,
                                                 merge_dir=merge_dir)
        conf.write(f'{merge_shell} 1G {stat_shells}\n')

        plot_shell = shell.generate_plot_shell(output_dir=output_dir,
                                               result_dir=merge_dir,
                                               shell_dir=shell_dir,
                                               plot_type=plot_type,
                                               processed_file=Path(f'processed_stats.{plot_type}.tsv').resolve())
        conf.write(f'{plot_shell} 1G {merge_shell}\n')
        
    if job:
        cmd = f'makejob {makejob_conf} -o {job}'
        if kwargs['no_check']:
            cmd += ' -no'
        util.logger.debug(f'>>> RUN:  {cmd}')
        assert not os.system(cmd)


if __name__ == '__main__':
    main()
