import datetime

today = datetime.date.today()
start_date = datetime.date(2011, 11, 01)
start_date_for_quarterly = start_date
week = datetime.timedelta(weeks=1)

name = "quarterly"
template_file = name + ".template"

f = open(template_file, "r")
f_txt = f.read()
f.close()

def get_quarter(mon):
    return (mon - 1)//3 + 1

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

while(1):
    if start_date > today:
        break

    year, month, day = start_date.timetuple()[:3]
    if month % 3 != 0:
        start_date = start_date + week
        continue
    # for vars()
    quarter = "%d-Q%d" % (year, get_quarter(month))
    start_ymd = "%d-%02d-%02d" % (year, month - 3, 1)
    end_ymd = str(last_day_of_month(start_date))
    replaced_txt = f_txt % vars()
    fname = str(year) + "-Q" + str(get_quarter(month))
    f2 = open(fname + ".txt", "w")
    f2.write(replaced_txt)
    f2.close()
    start_date = start_date + week
