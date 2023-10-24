
import os
import click
import textwrap

from combos_stat.plot.boxplot_tpl import generate_r_code
from combos_stat.plot.process_data import stat_from_result


__epilog__ = click.style('''\n
\b
examples:
    combos_stat plot -h
    combos_stat plot out/result
    combos_stat plot out/result --write boxplot.R
    combos_stat plot out/result --write boxplot.R --option x_lab=XXX --option width=30 --option dpi=500
''', fg='green')

@click.command(
    name='plot',
    no_args_is_help=True,
    help=click.style('Generate Boxplot with statistics results', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.argument('result_dir')
@click.option('-R', '--Rscript', help='Path to the executable Rscript', default='Rscript', show_default=True)
@click.option('-w', '--write', help='Write the R code to a file')
@click.option('--option', help='Options in the format key=value for boxplot, eg. title="Demo Stats", x_lab="Shared_Numbers", y_lab="Data"', multiple=True)
def main(**kwargs):
    r_script = kwargs['rscript']

    stat_from_result(kwargs['result_dir'])

    options = dict(option.split('=') for option in kwargs['option'])
    r_code = generate_r_code(**options)

    if kwargs['write']:
        with open(kwargs['write'], 'w') as f:
            f.write(r_code)

    cmd = textwrap.dedent(f'''{r_script} - <<EOF
    {r_code}EOF
    ''')
    try:
        assert not os.system(cmd)
    except Exception as e:
        print('ERROR', e)
