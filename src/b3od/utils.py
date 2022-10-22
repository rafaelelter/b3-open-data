from datetime import datetime, date


def parse_date(dt: any) -> date:
    """Parses a date from a string or a datetime object"""
    if isinstance(dt, date):
        return dt
    if isinstance(dt, datetime):
        return dt.date()
    if isinstance(dt, str):
        return date.fromisoformat(dt)
    raise ValueError(f"Invalid date format {dt}")
