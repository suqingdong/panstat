
import click

from combos_stat.stat import CombosStat


__epilog__ = click.style('''\n
\b
examples:
    combos_stat stat -h
    combos_stat stat -i input.txt -o output.txt -n 2
    combos_stat stat -i input.txt -o output.txt --header 
''', fg='green')

@click.command(
    name='stat',
    no_args_is_help=True,
    help=click.style('Calculate statistics', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.option('-i', '--input-file', help='Path to the input data file', type=click.Path(exists=True), required=True)
@click.option('-o', '--output-file', help='Path where the results will be saved', type=click.Path(), default='output_stat.txt', show_default=True)
@click.option('-n', '--num-samples', help='Number of samples to compute', type=int, required=True)
@click.option('-t', '--share_type', help='Type of share to compute', type=click.Choice(['intersection', 'union']), show_choices=True)
@click.option('--header', help='Row number to use as the column names', type=int, default=0, show_default=True)
@click.option('--sep', help='Delimiter to use for reading the input file (e.g., "\\t" for tab)', default='\t')
@click.option('--start-col', help='Column index to start reading sample data from', default=1, show_default=True, type=int)
@click.option('--show-process', help='Show process', is_flag=True)
def main(**kwargs):
    CombosStat(**kwargs).execute()
