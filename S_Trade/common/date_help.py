import datetime
from datetime import datetime, timedelta


def check_weekday(in_date=None):
    if in_date is None:
        return None
    if isinstance(in_date, datetime):
        return int(in_date.strftime('%w'))
    else:
        return None


def datetime_range(start=None, end=None):
    span = end - start
    for i in range(span.days + 1):
        yield start + timedelta(days=i)
