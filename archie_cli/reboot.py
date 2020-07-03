import click
from .helpers import validate_time
from archie import Archie
from .config import config_get


@click.group(name='reboot')
def reboot():
    """Reboot"""

    pass


@click.command(name="now")
def reboot_now():
    """Reboot router"""

    print('Reboot router')

    cfg = config_get()

    archie = Archie(host=cfg["host"],
                    username=cfg["username"],
                    password=cfg["password"])

    archie.login()
    # archie.reboot()


@click.command(name='schedule')
@click.argument('time', default=None, callback=validate_time)
def reboot_schedule(time):
    """Schedule router reboot"""

    print('schedule a cron job', time)


reboot.add_command(reboot_now)
reboot.add_command(reboot_schedule)
