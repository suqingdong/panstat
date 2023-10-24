
import click
from pathlib import Path


__epilog__ = click.style('''\n
\b
examples:
    combos_stat plot -h
''', fg='green')

@click.command(
    name='merge',
    no_args_is_help=True,
    help=click.style('Merge statistics results for each group', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.argument('result_dir')
@click.argument('-O', '--output-dir', help='The output directory')
def main(**kwargs):
    result_dir = Path(kwargs['result_dir'])
    # to do: merge each group results to a single file
