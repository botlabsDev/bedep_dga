import base64
import datetime
from pathlib import Path

import requests


class BedepError(RuntimeError):
    pass


def convert_config_to_dgarchive_dga_seed(config):
    usedTable = config['table'].split(".")[0]
    return f"bedep_dga" \
           f"_{hex(config['value1'])}" \
           f"_{hex(config['value2'])}" \
           f"_{hex(config['value3'])}" \
           f"_{usedTable}" \
           f"_{config['max_currencies']}"


def cache_file_from_url(url: str, cache_path: Path):
    cache_path.mkdir(exist_ok=True)
    cache_file = cache_path / url_to_file_name(url)
    if not cache_file.exists():
        request = requests.get(url)
        request.raise_for_status()
        cache_file.write_text(request.text)
    return cache_file


def url_to_file_name(url):
    return f"{base64.b64encode(url.encode()).decode()}_{datetime.datetime.now().strftime('%Y-%m-%d')}"


def next_wednesday(date=None):
    if date is None:
        date = datetime.datetime.today()
    current_weekday = date.weekday()
    days_till_wednesday = (14 - 5 - current_weekday) % 7
    return date_start() + datetime.timedelta(days=days_till_wednesday)


def next_thursday(date=None):
    if date is None:
        date = datetime.datetime.today()
    current_weekday = date.weekday()
    days_till_thursday = (14 - 4 - current_weekday) % 7
    return date_start() + datetime.timedelta(days=days_till_thursday)


def date_start(strDate=None):
    if not strDate:
        return (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        strDate = str(strDate).split(" ")[0]
        return datetime.datetime.strptime(strDate, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)


def date_end(strDate=None):
    if not strDate:
        return (datetime.datetime.today()).replace(hour=23, minute=59, second=59, microsecond=0)
    else:
        strDate = str(strDate).split(" ")[0]
        return datetime.datetime.strptime(strDate, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0)
