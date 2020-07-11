import logging
import time
import click

from .ping import ping
from .methods import archie_reboot


@click.group(name='watchdog')
def watchdog():
    """Watchdog"""


@click.command(name='install')
@click.option('--host', hidden=True, default='google.com',
              prompt='Hostname to ping', show_default=True)
@click.option('--period', hidden=True, default=60, type=click.IntRange(1),
              prompt='Watchdog period (seconds)', show_default=True)
def watchdog_install(host, period):
    """Install watchdog service"""

    print('Watchdog install', host, period)
    pass


@click.command(name='uninstall')
def watchdog_uninstall():
    """Uninstall watchdog service"""

    print('Watchdog uninstall')
    pass


@click.command(name='run', hidden=True)
@click.option('--host', default='google.com')
def watchdog_run(host):
    """Watchdog run"""

    logger = logging.getLogger('archie-cli')
    ping_failed = 0

    while ping_failed < 3:
        try:
            ttl, time_ms = ping(host)

            if time_ms < 100:
                logger.info(f"ping {host} ttl={ttl} time={time_ms} ms")
            elif time_ms < 1000:
                logger.warning(f"ping {host} ttl={ttl} time={time_ms} ms")
            else:
                logger.critical(f"ping {host} ttl={ttl} time={time_ms} ms")

            return True

        except Exception as e:
            logger.error(e)
            ping_failed += 1
            time.sleep(5)

    archie_reboot()


watchdog.add_command(watchdog_install)
watchdog.add_command(watchdog_uninstall)
watchdog.add_command(watchdog_run)
