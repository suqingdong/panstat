
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
                         
''', fg='green')

@click.command(
    name='plot',
    no_args_is_help=True,
    help=click.style('Plot statistics', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.argument('result_dir')
@click.option('-R', '--Rscript', help='Path to the executable Rscript', default='Rscript', show_default=True)
@click.option('-w', '--write', help='Write the R code to a file')
def main(**kwargs):

    r_script = kwargs['Rscript']

    stat_from_result(kwargs['result_dir'])

    r_code = generate_r_code()

    if kwargs['write']:
        with open(kwargs['write'], 'w') as f:
            f.write(r_code)

    cmd = textwrap.dedent(f'''{r_script} - <<EOF
    {r_code}EOF
    ''')
    try:
        assert not os.system(cmd)
    except Exception as e:
        print(r_code)
        print(e)
