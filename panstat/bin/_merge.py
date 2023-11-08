
import click

from panstat.util.merge import merge_result


__epilog__ = click.style('''\n
\b
examples:
    panstat merge -h
    panstat merge result -o merge_result
''', fg='green')


@click.command(
    name='merge',
    no_args_is_help=True,
    help=click.style('Merge statistics results', italic=True, fg='blue'),
    epilog=__epilog__,
)
@click.argument('result_dir')
@ click.option('-o', '--merge_dir',
               help='The output directory to store the merged results',
               default='merge', show_default=True)
def main(**kwargs):
    result_dir = kwargs['result_dir']
    merge_dir = kwargs['merge_dir']

    merge_result(result_dir=result_dir, merge_dir=merge_dir)
