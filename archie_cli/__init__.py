# from .ping import ping
# from archie import Archie
# import schedule

#global archie, logger
from .cli import cli





# def print_dot(seconds):
#     for i in range(seconds):
#         print('.', flush=True, end='')
#         time.sleep(1)
#     print()


# def reboot_router_job():
#     try:
#         archie.login()
#         archie.reboot()
#         logger.warning("Router is rebooting")
#         print_dot(seconds=60)
#     except Exception as e:
#         logger.error(e)


# def ping_google_job():
#     global ping_failed
#     host = config["ping_host"]
#
#     try:
#         ttl, time_ms = ping(host)
#
#         if time_ms < 100:
#             logger.info(f"ping {host} ttl={ttl} time={time_ms} ms")
#         elif time_ms < 1000:
#             logger.warning(f"ping {host} ttl={ttl} time={time_ms} ms")
#         else:
#             logger.critical(f"ping {host} ttl={ttl} time={time_ms} ms")
#
#     except Exception as e:
#         logger.error(e)
#         ping_failed = ping_failed + 1


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
