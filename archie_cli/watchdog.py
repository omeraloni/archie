import click


@click.group(name='watchdog')
def watchdog():
    """Watchdog"""


@click.command(name='install')
@click.option('--host', default='google.com', help='Hostname to ping')
@click.option('--period', default=10, help='Watchdog period (seconds)', type=click.IntRange(1))
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
def watchdog_run():
    """Watchdog run"""

    print('Watchdog run')


watchdog.add_command(watchdog_install)
watchdog.add_command(watchdog_uninstall)
watchdog.add_command(watchdog_run)
