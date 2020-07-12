import os
import re
import click
from crontab import CronTab

from .helpers import validate_time
from .methods import archie_reboot


@click.group(name='reboot')
def reboot():
    """Reboot"""

    pass


@click.command(name="now")
@click.pass_context
def reboot_now(ctx):
    """Reboot router"""

    archie_reboot(ctx.obj['debug'])


@click.group(name='schedule')
def reboot_schedule():
    """Schedule router reboot using crontab"""
    pass


@click.command(name='set')
@click.argument('time', default=None, callback=validate_time)
def schedule_set(time):
    """Set scheduled reboot"""

    result = re.fullmatch(r'(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]):([0-5][0-9])', time)
    hour, minute = result.group(1), result.group(2)

    cron = CronTab(user=os.environ.get('USER'))

    # Remove old job(s)
    jobs = cron.find_command("archie-cli reboot now")

    for job in jobs:
        cron.remove(job)

    job = cron.new(command="archie-cli reboot now")
    job.hours.on(hour)
    job.minute.on(minute)
    cron.write()

    print(f"Scheduled router reboot at {time}")


@click.command(name='clear')
def schedule_clear():
    """Clear scheduled reboot"""

    cron = CronTab(user=os.environ.get('USER'))

    # Remove old job(s)
    jobs = cron.find_command("archie-cli reboot now")

    for job in jobs:
        cron.remove(job)

    cron.write()

    print(f"Cleared scheduled router reboot")


@click.command(name='show')
def schedule_show():
    """Show current reboot"""

    cron = CronTab(user=os.environ.get('USER'))

    jobs = cron.find_command("archie-cli reboot now")

    for job in jobs:
        print(job)


@click.command(name='disable')
def schedule_disable():
    """Disable scheduled reboot"""

    cron = CronTab(user=os.environ.get('USER'))

    jobs = cron.find_command("archie reboot now")

    for job in jobs:
        if job.is_enabled() is False:
            print("Scheduled reboot already disabled")
        else:
            job.enable(False)
            cron.write()
            print("Disabled router scheduled reboot")


@click.command(name='enable')
def schedule_enable():
    """Enable scheduled reboot"""

    cron = CronTab(user=os.environ.get('USER'))

    jobs = cron.find_command("archie reboot now")

    for job in jobs:
        if job.is_enabled():
            print("Scheduled reboot already enabled")
        else:
            job.enable(True)
            cron.write()
            print("Enabled router scheduled reboot")


reboot_schedule.add_command(schedule_set)
reboot_schedule.add_command(schedule_clear)
reboot_schedule.add_command(schedule_show)
reboot_schedule.add_command(schedule_enable)
reboot_schedule.add_command(schedule_disable)

reboot.add_command(reboot_now)
reboot.add_command(reboot_schedule)
