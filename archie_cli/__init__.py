from .click_helpers import validate_time, validate_ip
from .helpers import ping
from archie import Archie
import logging
import schedule
import time
import click

global archie, config, ping_failed, logger


def setup_logging():
    global logger
    logger = logging.getLogger('archie-cli')
    logger.setLevel(logging.DEBUG)

    console_logger = logging.StreamHandler()
    console_logger.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    console_logger.setLevel(logging.DEBUG)
    logger.addHandler(console_logger)

    file_logger = logging.FileHandler('archie.log')
    file_logger.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_logger.setLevel(logging.DEBUG)
    logger.addHandler(file_logger)


def print_dot(seconds):
    for i in range(seconds):
        print('.', flush=True, end='')
        time.sleep(1)
    print()


def reboot_router_job():
    try:
        #archie.login()
        #archie.reboot()
        logger.info("Router is rebooting")
        print_dot(seconds=30)
    except Exception as err:
        logger.error(err)


def ping_google_job():
    global ping_failed
    host = config["ping_host"]

    try:
        result = ping(host)
        logger.info(f"ping {host} ttl={result[0]} time={result[1]} ms")
    except Exception as err:
        logger.error(err)
        ping_failed = ping_failed + 1

    '''
    if ping_failed > 3:
        reboot_router_job()
        ping_failed = 0
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
