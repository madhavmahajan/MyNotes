"""
Description: Utilities module to support various other methods and operations
"""

import datetime
import re

from django.utils.safestring import mark_safe

from . import constants


def get_todays_date():
    """Return today's date in form of a tuple

    Returns:
        (year, month, day)
    """
    now = datetime.datetime.now()
    return now.year, now.month, now.day


def get_formatted_date(year=None, month=None, day=None):
    """Returns formatted date to display properly in UI

    Args:
        year (int): Year
        month (int): Month
        day (int): Day

    Returns:
        Date in format "year/month/day"
    """
    if year and month and day:
        return "{}/{}/{}".format(year, month, day)
    year, month, day = get_todays_date()
    return "{}/{}/{}".format(year, month, day)


def convert_epoch_to_datetime(epoch_time):
    """Convert epoch time to user friendly date-time formatted string

    Args:
        epoch_time (int): Epoch time

    Returns:
         Date-time string in '%Y-%m-%d %H:%M:%S' format
    """
    return datetime.datetime.fromtimestamp(epoch_time).strftime(constants.DISPLAY_DATETIME_FORMAT)


def generate_notes_file_name(year, month, day):
    """Generate note's file name for a particular date

    Args:
        year (int): Year
        month (int): Month
        day (int): Day

    Returns:
        Note name
    """
    return "{}-{}-{}".format(year, month, day)


def format_certain_string_in_content(content, string, case_insensitive=True):
    """Format string with string in the content to mark it as bold and italics

    Args:
        content (str): Content that needs to be formatted
        string (str): Part of content that needs to be formatted
        case_insensitive (bool): Flag to replace string case-insensitively

    Returns:
        Formatted string and marked safe for HTML output purposes
    """
    new_string = "<i><strong>{}</strong></i>".format(string)
    if case_insensitive:
        data = re.sub(string, new_string, content, flags=re.I)
    else:
        data = re.sub(string, new_string, content)
    return mark_safe(data)
