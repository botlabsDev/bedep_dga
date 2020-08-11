import base64
import datetime
from pathlib import Path

import requests


def get_dgarchive_dga_name(config):
    usedTable = config['table'].split(".")[0]
    return f"bedep_dga" \
           f"_{hex(config['value1'])}" \
           f"_{hex(config['value2'])}" \
           f"_{hex(config['value3'])}" \
           f"_{usedTable}" \
           f"_{config['max_currencies']}"


def cache_file(url: str, cacheFolder: Path):
    cacheFolder.mkdir(exist_ok=True)

    filename = f"{base64.b64encode(url.encode()).decode()}_{datetime.datetime.now().strftime('%Y-%m-%d')}"
    cacheFolder = cacheFolder / filename

    if not cacheFolder.exists():
        request = requests.get(url)
        cacheFolder.write_text(request.text)
    return cacheFolder


def next_thursday():
    current_weekday = datetime.datetime.today().weekday()
    days_till_wednesday = (14 - 4 - current_weekday) % 7
    return date_start() + datetime.timedelta(days=days_till_wednesday)


def date_start(input=None):
    if not input:
        return (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        input = str(input).split(" ")[0]
        return datetime.datetime.strptime(input, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)


def date_end(input=None):
    if not input:
        return (datetime.datetime.today()).replace(hour=23, minute=59, second=59, microsecond=0)
    else:
        return datetime.datetime.strptime(input, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0)