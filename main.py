import datetime
from typing import Iterable

from icalevents.icalevents import events


def dates_from_ics(ical_url: str):
    return events(ical_url, fix_apple=True)


def main(no_working_days: int, free_days: Iterable[datetime.datetime]):
    assert 0 < no_working_days < 7


if __name__ == "__main__":
    sax19 = "https://www.ferienwiki.de/exports/ferien/2019/de/sachsen"
    sax20 = "https://www.ferienwiki.de/exports/ferien/2020/de/sachsen"
    events = dates_from_ics(sax20)
    main(3, [])
