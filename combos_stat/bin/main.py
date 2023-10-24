import click

from combos_stat import version_info
from ._stat import main as stat_cli
from ._plot import main as plot_cli
from ._batch import main as batch_cli


CONTEXT_SETTINGS = dict(
    help_option_names=['-?', '-h', '--help'],
    max_content_width=120,
)


@click.group(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='green', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
    epilog=click.style('''contact: {author} <{author_email}>''', fg='yellow').format(**version_info),
)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
def cli(**kwargs):
    pass


def main():
    cli.add_command(stat_cli)
    cli.add_command(plot_cli)
    cli.add_command(batch_cli)
    cli()


if __name__ == '__main__':
    main()
