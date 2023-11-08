
import os
import click
import textwrap

from panstat.util.merge import merge_result


__epilog__ = click.style('''\n
\b
examples:
    panstat merge -h
''', fg='green')


@click.command(
    name='merge',
    no_args_is_help=True,
    help=click.style('Merge statistics results', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.argument('result_dir')
@ click.option('-o', '--out_dir',
               help='The output directory to store the merged results',
               default='merge', show_default=True)
def main(**kwargs):
    result_dir = kwargs['result_dir']
    out_dir = kwargs['out_dir']

    merge_result(result_dir=result_dir, out_dir=out_dir)