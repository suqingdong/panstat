
import os
import click
import textwrap

from combos_stat.plot.boxplot_tpl import generate_r_code as generate_boxplot_r_code
from combos_stat.plot.pointplot_tpl import generate_r_code as generate_pointplot_r_code
from combos_stat.plot.process_data import stat_from_result
from combos_stat import util


__epilog__ = click.style('''\n
\b
examples:
    combos_stat plot -h
    combos_stat plot out/result
    combos_stat plot out/result --write pointplot.R
    combos_stat plot out/result --write pointplot.R --option x_lab=XXX --option width=30 --option dpi=500
    combos_stat plot out/result --write boxplot.R --plot-type box 

\b
default options:
    infile = 'processed_stats.tsv'
    output = 'pointplot'
    x_lab = 'Genomes'
    y_lab = 'Families'
    title = ''
    legend_title = 'Type'
    dpi = 300
    width = 14
    height = 7
''', fg='green')


@click.command(
    name='plot',
    no_args_is_help=True,
    help=click.style('Generate Boxplot/Pointplot with statistics results',
                     italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.argument('result_dir')
@click.option('-R', '--Rscript',
              help='Path to the executable Rscript',
              default='Rscript',
              show_default=True)
@click.option('-w', '--write',
              help='Write the R code to a file',
              default='boxplot.R',
              show_default=True)
@click.option('-T', '--plot-type',
              help='The type of plot',
              type=click.Choice(['point', 'box']),
              default='point',
              show_default=True,
              show_choices=True)
@ click.option('--option',
               help='Options in the format key=value for plot, eg. title="Demo Stats", x_lab="Shared_Numbers", y_lab="Data"',
               multiple=True)
def main(**kwargs):
    r_script = kwargs['rscript']
    plot_type = kwargs['plot_type']

    options = dict(option.split('=') for option in kwargs['option'])
    processed_file = options.get('infile', 'processed_stats.tsv')

    stat_from_result(kwargs['result_dir'], outfile=processed_file, plot_type=plot_type)
    if plot_type == 'point':
        r_code = generate_pointplot_r_code(**options)
    else:
        r_code = generate_boxplot_r_code(**options)

    with open(kwargs['write'], 'w') as f:
        f.write(r_code)
    util.logger.debug(f'saved R code to: {kwargs["write"]}')

    try:
        cmd = f'{r_script} {kwargs["write"]}'
        util.logger.debug(f'Drawing {plot_type}plot ...')
        assert not os.system(cmd)
    except Exception as e:
        print('ERROR', e)
