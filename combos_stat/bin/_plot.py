
import click

__epilog__ = click.style('''\n
\b
examples:
    combos_stat plot -h
''', fg='green')

@click.command(
    name='plot',
    no_args_is_help=True,
    help=click.style('Plot statistics', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.option('-i', '--input-file', help='Path to the input data file', type=click.Path(exists=True), required=True)
def main(**kwargs):
    pass
