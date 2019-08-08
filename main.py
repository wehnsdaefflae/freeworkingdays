from math import sqrt, pi, exp

import requests
import datetime
from typing import List, Optional, Union, Sequence, Tuple

from matplotlib import pyplot

from ics import Calendar


def get_calendar_from_url(url: str) -> Calendar:
    ics = requests.get(url)
    return Calendar(ics.text)


def merge_events(*calendars: Calendar) -> Calendar:
    calendar = Calendar()

    c_events = calendar.events
    for each_calendar in calendars:
        for each_event in each_calendar.events:
            c_events.add(each_event)

    return calendar


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


def show_holidays(calendar: Calendar, time_start: Optional[datetime.date] = None, time_end: Optional[datetime.date] = None) -> str:
    weekdays = "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    lines = []

    for each_holiday in sorted(calendar.events, key=lambda _x: _x.begin):
        assert each_holiday.duration == datetime.timedelta(days=1)

        each_day = weekdays[each_holiday.begin.weekday()]

        if time_start is None and time_end is None:
            lines.append(f"{each_holiday.description[:20]:>20s}: {each_day:>10s}")

        elif time_start is None and each_holiday.begin.date() < time_end:
            lines.append(f"{each_holiday.description[:20]:>20s}: {each_day:>10s}")

        elif time_end is None and each_holiday.begin.date() >= time_start:
            lines.append(f"{each_holiday.description[:20]:>20s}: {each_day:>10s}")

        elif time_start <= each_holiday.begin.date() < time_end:
            lines.append(f"{each_holiday.description[:20]:>20s}: {each_day:>10s}")

    return "\n".join(lines)


def gaussian(x, mu, sig):
    return 1. / (sqrt(2. * pi) * sig) * exp(-pow((x - mu) / sig, 2.) / 2.)


def gaussian_blur(time_series: List[float], window_size: int = 5) -> List[float]:
    length = len(time_series)
    new_list = [0.] * window_size
    for i in range(window_size + 1, length - window_size):
        pass


def blur_time_series(time_series: List[float], window_size: int = 5) -> List[float]:
    l_seq = len(time_series)
    new_series = [.0 for _ in time_series]
    for _i in range(window_size, l_seq - window_size):
        new_series[_i] = sum(time_series[_i - window_size:_i + window_size]) / (2. * window_size + 1.)
    return new_series


def plot_holiday_density_per_weekday(calendar: Calendar, time_start: Optional[datetime.date] = None, time_end: Optional[datetime.date] = None, reverse: bool = False):
    sorted_events = sorted(calendar.events, key=lambda _x: _x.begin)
    date_event_first = sorted_events[0].begin.date()
    date_event_last = sorted_events[-1].begin.date()

    if time_start is None or time_start < date_event_first:
        time_start = date_event_first

    if time_end is None or date_event_last < time_end:
        time_end = date_event_last

    date_range = [time_start + datetime.timedelta(days=_x) for _x in range((time_end - time_start).days)]

    holidates = {_e.begin.date() for _e in sorted_events}

    pyplot.subplot(211)

    labels = "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    holimondays = [float(_d in holidates and _d.weekday() == 0) for _d in date_range]
    holimondays = blur_time_series(holimondays)
    #pyplot.plot(date_range, holimondays, label="monday", alpha=.5)

    holituesdays = [float(_d in holidates and _d.weekday() == 1) for _d in date_range]
    holituesdays = blur_time_series(holituesdays)
    #pyplot.plot(date_range, holituesdays, label="tuesday", alpha=.5)

    holiwednesdays = [float(_d in holidates and _d.weekday() == 2) for _d in date_range]
    holiwednesdays = blur_time_series(holiwednesdays)
    #pyplot.plot(date_range, holiwednesdays, label="wednesday", alpha=.5)

    holithursdays = [float(_d in holidates and _d.weekday() == 3) for _d in date_range]
    holithursdays = blur_time_series(holithursdays)
    #pyplot.plot(date_range, holithursdays, label="thursday", alpha=.5)

    holifridays = [float(_d in holidates and _d.weekday() == 4) for _d in date_range]
    holifridays = blur_time_series(holifridays)
    #pyplot.plot(date_range, holifridays, label="friday", alpha=.5)

    holisaturdays = [float(_d in holidates and _d.weekday() == 5) for _d in date_range]
    holisaturdays = blur_time_series(holisaturdays)
    #pyplot.plot(date_range, holisaturdays, label="saturday", alpha=.5)

    holisundays = [float(_d in holidates and _d.weekday() == 6) for _d in date_range]
    holisundays = blur_time_series(holisundays)
    #pyplot.plot(date_range, holisundays, label="sunday", alpha=.5)

    pyplot.stackplot(date_range, holimondays, holituesdays, holiwednesdays, holithursdays, holifridays, holisaturdays, holisundays, labels=labels)

    pyplot.legend()

    pyplot.subplot(212)
    total = [sum(_x) for _x in zip(holimondays, holituesdays, holiwednesdays, holithursdays, holifridays, holisaturdays, holisundays)]
    pyplot.plot(date_range, total)

    pyplot.legend()
    pyplot.show()



def main():
    sax19 = "https://www.ferienwiki.de/exports/feiertage/2019/de/sachsen"
    sax20 = "https://www.ferienwiki.de/exports/feiertage/2020/de/sachsen"

    calendar_urls = sax19, sax20

    calendars = tuple(get_calendar_from_url(_url) for _url in calendar_urls)
    calendar_full = merge_events(*calendars)

    start_date = datetime.date(2019, 10, 1)
    # end_date  = datetime.date(2020, 5, 1)
    end_date = datetime.date(2020, 10, 1)

    plot_holiday_density_per_weekday(calendar_full, time_start=start_date, time_end=end_date)


def _main():
    sax19 = "https://www.ferienwiki.de/exports/feiertage/2019/de/sachsen"
    sax20 = "https://www.ferienwiki.de/exports/feiertage/2020/de/sachsen"

    bav19 = "https://www.ferienwiki.de/exports/feiertage/2019/de/bayern"
    bav20 = "https://www.ferienwiki.de/exports/feiertage/2020/de/bayern"

    calendar_urls = sax19, sax20
    # calendar_urls = bav19, bav20

    calendars = tuple(get_calendar_from_url(_url) for _url in calendar_urls)
    calendar_full = merge_events(*calendars)

    start_date = datetime.date(2019, 10, 1)
    end_date = datetime.date(2020, 5, 1)

    # start_date = datetime.date(2018, 3, 1)
    # end_date = datetime.date(2019, 10, 1)

    free_days = most_free_days(calendar_full, time_start=start_date, time_end=end_date)

    print("\n".join(f"{_x[0]:>10s}\t{_x[1]:>3d}" for _x in free_days))

    print(show_holidays(calendar_full, time_start=start_date, time_end=end_date))


if __name__ == "__main__":
    main()
