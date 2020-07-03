import json
import os
from .click_helpers import validate_time, validate_ip
from .ping import ping
# from archie import Archie
import logging
import schedule
import time
import click
import coloredlogs

global archie, logger


def setup_logging():
    global logger
    logger = logging.getLogger('archie-cli')
    coloredlogs.install(logger=logger, level=logging.DEBUG,
                        fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

    file_logger = logging.FileHandler('archie.log')
    file_logger.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
    file_logger.setLevel(logging.DEBUG)
    logger.addHandler(file_logger)


def print_dot(seconds):
    for i in range(seconds):
        print('.', flush=True, end='')
        time.sleep(1)
    print()


def reboot_router_job():
    try:
        archie.login()
        archie.reboot()
        logger.warning("Router is rebooting")
        print_dot(seconds=60)
    except Exception as e:
        logger.error(e)


def ping_google_job():
    global ping_failed
    host = config["ping_host"]

    try:
        ttl, time_ms = ping(host)

        if time_ms < 100:
            logger.info(f"ping {host} ttl={ttl} time={time_ms} ms")
        elif time_ms < 1000:
            logger.warning(f"ping {host} ttl={ttl} time={time_ms} ms")
        else:
            logger.critical(f"ping {host} ttl={ttl} time={time_ms} ms")

    except Exception as e:
        logger.error(e)
        ping_failed = ping_failed + 1

    '''
    if ping_failed > 3:
        reboot_router_job()
        ping_failed = 0
    '''


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """TP-Link Archer C7 CLI"""

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug

    setup_logging()


@click.group(name='config')
def config():
    """Configure router login details"""
    pass


@click.command(name='set')
@click.option('--host', hidden=True, default='192.168.0.1', envvar='ARCHIE_HOSTNAME', help='Router\'s IP address',
              prompt='Router\'s IP address', callback=validate_ip, show_default=True)
@click.option('--username', hidden=True, default='admin', envvar='ARCHIE_USERNAME', help='Router\'s admin user name',
              prompt='Router\'s admin user name', show_default=True)
@click.option('--password', hidden=True, default='admin', envvar='ARCHIE_PASSWORD',
              help='Router\'s admin user password',
              prompt='Router\'s admin user password', show_default=True, hide_input=True, confirmation_prompt=True)
@click.option('--save', is_flag=True, default=True, hidden=True, prompt='Save', callback=abort_if_false)
@click.pass_context
def config_set(host, username, password, save):
    """Set router login details"""

    location = os.environ.get('HOME', '') + '/.config/archie'

    if os.path.exists(location) is False:
        os.mkdir(location)

    os.chdir(location)
    with open('config.json', 'w') as file:
        cfg = {
            'host': host,
            'username': username,
            'password': password
        }

        json.dump(cfg, file)
        print('Saved!')


@click.command(name='show')
@click.pass_context
def config_show():
    """Set router login details"""

    location = os.environ.get('HOME', '') + '/.config/archie'
    if os.path.exists(location) is False:
        print('No configuration saved')
        ctx.abort()

    os.chdir(location)

    if os.path.isfile('config.json') is False:
        print('No configuration saved')
        ctx.abort()

    with open('config.json', 'r') as file:
        cfg = json.load(file)
        print(cfg)


config.add_command(config_set)
config.add_command(config_show)


@click.command(name='watchdog')
@click.option('--host', default='google.com', help='Hostname to ping')
@click.option('--period', default=10, help='Watchdog period (seconds)', type=click.IntRange(1), )
def watchdog(host, period):
    """Install a watchdog cron job"""

    logger.info(host, period)
    pass


@click.group(name='reboot')
def reboot():
    """Reboot"""

    pass


@click.command(name="now")
def reboot_now():
    """Reboot router"""

    print('Reboot router')


@click.command(name='schedule')
@click.argument('time', default=None, callback=validate_time)
def reboot_schedule(time):
    """Schedule router reboot"""

    print('schedule a cron job', time)


reboot.add_command(reboot_now)
reboot.add_command(reboot_schedule)

cli.add_command(config)
cli.add_command(watchdog)
cli.add_command(reboot)


'''
@click.command()
@click.option('--host',         default='192.168.0.1',  envvar='ARCHIE_HOSTNAME',   help='Archer\'s IP address',
              callback=validate_ip)
@click.option('--username',     default='admin',        envvar='ARCHIE_USERNAME',   help='Archer\'s admin user name')
@click.option('--password',     default='admin',        envvar='ARCHIE_PASSWORD',   help='Archer\'s admin user password')
@click.option('--ping_host',    default='google.com',                               help='Ping host name')
@click.option('--ping_period',  default=10,             type=click.IntRange(1),     help='Ping period (seconds)')
@click.option('--reboot',       default=None,                                       help='Scheduled reboot time',
              callback=validate_time)
def archie_cli(host, username, password, ping_host, ping_period, reboot):
    global archie, ping_failed, config, logger

    setup_logging()
    logger = logging.getLogger('archie-cli')

    ping_failed = 0

    config = {
        "host": host,
        "username": username,
        "password": password,
        "ping_host": ping_host,
        "ping_period": ping_period,
        "reboot_schedule": reboot
    }

    logger.debug(config)

    archie = Archie(host, username, password, test_mode=True)

    if config["reboot_schedule"] is not None:
        schedule.every().day.at(config["reboot_schedule"]).do(reboot_router_job)

    schedule.every(config["ping_period"]).seconds.do(ping_google_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
'''
