import click
import logging
import coloredlogs

from .config import config
from .reboot import reboot
from .watchdog import watchdog


def setup_logging():
    logger = logging.getLogger('archie-cli')
    coloredlogs.install(logger=logger, level=logging.DEBUG,
                        fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

    file_logger = logging.FileHandler('logs/archie.log')
    file_logger.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
    file_logger.setLevel(logging.DEBUG)
    logger.addHandler(file_logger)


@click.group()
@click.option('--debug', is_flag=True, default=False)
@click.version_option(version=None)  # FIXME: only works if installed via pip, why?
@click.pass_context
def cli(ctx, debug):
    """TP-Link Archer C7 CLI"""

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug

    setup_logging()


cli.add_command(config)
cli.add_command(watchdog)
cli.add_command(reboot)
