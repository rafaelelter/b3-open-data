"""Usefull functions of the application"""

from datetime import datetime, date


def parse_date(date_to_parse: any) -> date:
    """Parses a date from a string or a datetime object"""
    if isinstance(date_to_parse, date):
        return date_to_parse
    if isinstance(date_to_parse, datetime):
        return date_to_parse.date()
    if isinstance(date_to_parse, str):
        return date.fromisoformat(date_to_parse)
    raise ValueError(f"Invalid date format {date_to_parse}")
