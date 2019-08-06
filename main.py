import requests
import datetime
from typing import List, Optional, Union

from ics import Calendar


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
    return Calendar(ics.text)


def most_free_days(calendar: Calendar, time_start: Optional[datetime.date] = None, time_end: Optional[datetime.date] = None) -> List[List[Union[str, int]]]:
    free_weekdays = ["monday", 0], ["tuesday", 0], ["wednesday", 0], ["thursday", 0], ["friday", 0], ["saturday", 0], ["sunday", 0]

    for each_holiday in calendar.events:
        each_weekday = each_holiday.begin.weekday()

        assert each_holiday.duration == datetime.timedelta(days=1)

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

    bav19 = "https://www.ferienwiki.de/exports/feiertage/2019/de/bayern"
    bav20 = "https://www.ferienwiki.de/exports/feiertage/2020/de/bayern"

    calendar_urls = sax19, sax20
    # calendar_urls = bav19, bav20

    calendars = tuple(get_calendar_from_url(_url) for _url in calendar_urls)
    calendar_full = merge_events(*calendars)

    start_date = datetime.date(2019, 10, 1)
    # end_date = datetime.date(2020, 5, 1)
    end_date = datetime.date(2020, 12, 30)

    # start_date = datetime.date(2018, 3, 1)
    # end_date = datetime.date(2019, 10, 1)

    free_days = most_free_days(calendar_full, time_start=start_date, time_end=end_date)
    print("\n".join(f"{_x[0]:>10s}\t{_x[1]:>3d}" for _x in free_days))


if __name__ == "__main__":
    main()
