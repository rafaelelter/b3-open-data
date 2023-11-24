"""Usefull functions of the application"""

from datetime import datetime, date
from typing import Any


def parse_date(date_to_parse: Any) -> date:
    """Parses a date from a string or a datetime object"""
    if isinstance(date_to_parse, date):
        return date_to_parse
    if isinstance(date_to_parse, datetime):
        return date_to_parse.date()
    if isinstance(date_to_parse, str):
        return date.fromisoformat(date_to_parse)
    raise ValueError(f"Invalid date format {date_to_parse}")


def is_string(seq: Any) -> bool:
    """Checks if a variable is a string"""
    return isinstance(seq, str)


def is_sequence(seq: Any) -> bool:
    """Checks if a variable is a sequence"""

    if is_string(seq):
        return False
    try:
        len(seq)
    except TypeError:
        return False
    return True
