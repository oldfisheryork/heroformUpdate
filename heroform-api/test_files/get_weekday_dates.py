# from datetime import timedelta, date
import datetime as dt
import calendar


def add_front_start_date(start_year, start_month, start_day, end_year, end_month, end_day):
    first_day_id = calendar.weekday(start_year, start_month, start_day)
    start_dt = dt.date(start_year, start_month, start_day)
    end_dt = dt.date(end_year, end_month, end_day)

    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + dt.timedelta(n)


    flag = start_dt.weekday()
    weekday_list = []

    for i in range(flag):
        weekday_list.append(calendar.day_name[i])

    for each_day in daterange(start_dt, end_dt):
        if each_day.weekday() < 5:
            weekday_list.append(each_day.strftime("%A, %B %d %Y"))

    # is for printing
    # for day in weekday_list:
    #     print(day)
    return weekday_list

start_year = 2019
start_month = 6
start_day = 7

end_year = 2019
end_month = 7
end_day = 24

add_front_start_date(start_year, start_month, start_day, end_year, end_month, end_day)