import random

from datetime import timedelta, date
from dateutil.relativedelta import relativedelta


def yield_dates(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def get_date_values():
    start_date = date.today() - relativedelta(years=5)
    end_date = date.today()
    date_range_list = [dt.strftime("%Y-%m-%d") for dt in yield_dates(start_date, end_date)]
    result = [{"date": v, "value": random.randint(100, 200)} for v in date_range_list]
    return result
