import logging
import os
import re
import click
from crontab import CronTab

from .helpers import validate_time
from .functions import archie_reboot


@click.group(name='reboot')
def reboot():
    """Reboot"""

    pass


@click.command(name="now")
def reboot_now():
    """Reboot router"""

    archie_reboot()


@click.group(name='schedule')
def reboot_schedule():
    """Scheduled router reboot"""
    pass


@click.command(name='set')
@click.argument('time', default=None, callback=validate_time)
def set_schedule(time):
    """Set router scheduled reboot"""

    result = re.fullmatch(r'(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]):([0-5][0-9])', time)
    hour, minute = result.group(1), result.group(2)

    cron = CronTab(user=os.environ.get('USER'))

    # Remove old job
    job = cron.find_command("archie reboot now")
    cron.remove(job)

    job = cron.new(command="archie reboot now", comment=f"arhcie-cli.reboot.schedule@{time}")
    job.hours.on(hour)
    job.minute.on(minute)
    cron.write()

    print(f"Scheduled router reboot at {time}")


@click.command(name='show')
def schedule_show():
    """Show current reboot schedule"""

    cron = CronTab(user=os.environ.get('USER'))

    jobs = cron.find_command("archie reboot now")

    for job in jobs:
        text = str(job)
        result = re.fullmatch(r'(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]):([0-5][0-9])', text)
        time = result.group(1)
        print(f"Scheduled reboot set to {time}")


@click.command(name='disable')
def schedule_disable():
    """Disable scheduled router reboot"""

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
def enable_schedule():
    """Enable scheduled router reboot"""

    cron = CronTab(user=os.environ.get('USER'))

    jobs = cron.find_command("archie reboot now")

    for job in jobs:
        if job.is_enabled():
            print("Scheduled reboot already enabled")
        else:
            job.enable(True)
            cron.write()
            print("Enabled router scheduled reboot")


reboot_schedule.add_command(set_schedule)
reboot_schedule.add_command(schedule_show)
reboot_schedule.add_command(enable_schedule)
reboot_schedule.add_command(schedule_disable)

reboot.add_command(reboot_now)
reboot.add_command(reboot_schedule)
