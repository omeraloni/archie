import logging
import os
import time
import click
from crontab import CronTab

from .ping import ping
from .methods import archie_reboot
from .helpers import abort_if_false


@click.group(name='watchdog')
def watchdog():
    """Watchdog"""


@click.command(name='install')
@click.option('--interface', default='wlan0',
              prompt='Interface to watch', show_default=True)
@click.option('--host', default='google.com',
              prompt='Hostname to ping', show_default=True)
@click.option('--period', default=2, type=click.IntRange(1),
              prompt='Watch period (minutes)', show_default=True)
@click.option('--save', is_flag=True, default=True, hidden=True, prompt='Save', callback=abort_if_false)
def watchdog_install(interface, host, period, save):
    """Install watchdog service"""

    cron = CronTab(user=os.environ.get('USER'))

    # Remove old job(s)
    jobs = cron.find_command("archie-cli watchdog run")

    for job in jobs:
        cron.remove(job)

    job = cron.new(command=f"archie-cli watchdog run --interface={interface} --host={host}c")

    job.minute.every(period)
    cron.write()

    print(f"Watchdog set to watch {interface}, will ping {host} every {period} minutes")


@click.command(name='uninstall')
def watchdog_uninstall():
    """Uninstall watchdog service"""

    cron = CronTab(user=os.environ.get('USER'))

    jobs = cron.find_command("archie-cli watchdog run")

    for job in jobs:
        cron.remove(job)

    cron.write()


@click.command(name='show')
def watchdog_show():
    """Show current watchdog cron task"""

    cron = CronTab(user=os.environ.get('USER'))

    jobs = cron.find_command("archie-cli watchdog run")

    for job in jobs:
        print(job)


@click.command(name='run', hidden=True)
@click.option('--interface', default='wlan0')
@click.option('--host', default='google.com')
def watchdog_run(interface, host):
    """Watchdog run"""

    logger = logging.getLogger('archie-cli')

    retries = 0

    while retries < 3:
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
            retries += 1
            logger.error(f"ping retry {retries} failed ({e})")
            time.sleep(5)

    archie_reboot()


watchdog.add_command(watchdog_install)
watchdog.add_command(watchdog_uninstall)
watchdog.add_command(watchdog_show)
watchdog.add_command(watchdog_run)
