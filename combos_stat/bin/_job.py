
import tempfile
import click


__epilog__ = click.style('''\n
\b
examples:
    combos_stat stat -h
''', fg='green')

@click.command(
    name='job',
    no_args_is_help=True,
    help=click.style('Create SJM Job', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.option('-i', '--input-file', help='Path to the input data file', type=click.Path(exists=True), required=True)
@click.option('-l', '--lines', help='the number of lines to split', type=int)
# @click.option('-o', '--output-file', help='Path to the output data file', type=click.Path(), required=True)
def main(**kwargs):
    tempfile
