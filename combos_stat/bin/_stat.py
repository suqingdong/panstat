
import click

from combos_stat.stat import CombosStat


__epilog__ = click.style('''\n
\b
examples:
    combos_stat stat -h
    combos_stat stat -i input.txt -o output.txt -n 13 -t intersection
    combos_stat stat -i input.txt -o output.txt -n 13 -t intersection --chunksize 100 --chunk 2 [read 101-200 lines]
''', fg='green')

@click.command(
    name='stat',
    no_args_is_help=True,
    help=click.style('Calculate statistics for shared data counts based on combinations of samples.', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.option('-i', '--input-file', help='Path to the input data file', type=click.Path(exists=True), required=True)
@click.option('-o', '--output-file', help='Path where the results will be saved', type=click.Path(), default='output_stat.txt', show_default=True)
@click.option('-n', '--num-samples', help='Number of samples to compute', type=int, required=True)
@click.option('-t', '--share_type', help='Type of share to compute', type=click.Choice(['intersection', 'union']), show_choices=True)
@click.option('--header', help='Row number to use as the column names', type=int, default=0, show_default=True)
@click.option('--sep', help='Delimiter to use for reading the input file (e.g., "\\t" for tab)', default='\t')
@click.option('--start-col', help='Column index to start reading sample data from', default=1, show_default=True, type=int)
@click.option('--show-progress', help='Show progress', type=click.BOOL, default=True)
@click.option('--chunksize', help='The chunksize lines to read', type=int)
@click.option('--chunk', help='The index of chunk', type=int)
def main(**kwargs):
    combos = CombosStat(**kwargs)
    results = combos.compute()
    combos.save(results, kwargs['output_file'])
