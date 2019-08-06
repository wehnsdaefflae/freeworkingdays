import requests
import datetime
from typing import Iterable, Tuple, List, Optional, Union

from icalevents.icalevents import events
from ics import Calendar


def dates_from_ics(ical_url: str):
    return events(ical_url, fix_apple=True)


def is_free(day: datetime.datetime) -> bool:
    return False


def get_free_days(free_days: Iterable[datetime.datetime]) -> Tuple[int, int, int, int, int, int, int]:
    weekdays_off = [0, 0, 0, 0, 0, 0, 0]
    for each_day in free_days:
        if is_free(each_day):
            weekdays_off[each_day] += 1
    return tuple(weekdays_off)


def merge_events(*calendars: Calendar) -> Calendar:
    calendar = Calendar()
    c_events = calendar.events
    for each_calendar in calendars:
        each_events = each_calendar.events
        for each_event in each_events:
            c_events.add(each_event)
    return calendar


def get_calendar_from_url(url: str) -> Calendar:
    ics = requests.get(url)
    ics_text = ics.text
    return Calendar(ics_text)


def most_free_days(calendar: Calendar, time_start: Optional[datetime.date] = None, time_end: Optional[datetime.date] = None) -> List[List[Union[str, int]]]:
    free_weekdays = ["monday", 0], ["tuesday", 0], ["wednesday", 0], ["thursday", 0], ["friday", 0], ["saturday", 0], ["sunday", 0]

    # holidays = sorted(calendar.events, key=lambda _x: _x.begin)
    for each_holiday in calendar.events:
        each_weekday = each_holiday.begin.weekday()

        if time_start is None and time_end is None:
            free_weekdays[each_weekday][-1] += 1

        elif time_start is None and each_holiday.begin.date() < time_end:
            free_weekdays[each_weekday][-1] += 1

        elif time_end is None and each_holiday.begin.date() >= time_start:
            free_weekdays[each_weekday][-1] += 1

        elif time_start <= each_holiday.begin.date() < time_end:
            free_weekdays[each_weekday][-1] += 1

    return sorted(free_weekdays, key=lambda _x: -_x[-1])


def main():
    sax19 = "https://www.ferienwiki.de/exports/feiertage/2019/de/sachsen"
    sax20 = "https://www.ferienwiki.de/exports/feiertage/2020/de/sachsen"

    calendar_urls = sax19, sax20

    calendars = tuple(get_calendar_from_url(_url) for _url in calendar_urls)
    calendar_full = merge_events(*calendars)

    free_days = most_free_days(calendar_full, time_start=datetime.date(2019, 10, 1), time_end=datetime.date(2020, 5, 1))
    print("\n".join(f"{_x[0]:>10s}\t{_x[1]:>3d}" for _x in free_days))


if __name__ == "__main__":
    main()
