import datetime
start_date = datetime.date(2011, 10, 31)
start_date_for_weekly = start_date
t_end_date = datetime.date(2012, 06, 11)
week = datetime.timedelta(weeks=1)

template_file = ".template"
f = open(template_file, "r")
f_txt = f.read()

while (1):
    if start_date > t_end_date:
        break

    end_date = start_date + datetime.timedelta(days=6)
    replaced_txt = f_txt % vars()
    f2 = open(str(start_date) + ".txt", "w")
    f2.write(replaced_txt)
    f2.close
    start_date = start_date + week
    if (start_date_for_weekly + (10 * week)) == start_date:
        start_date_for_weekly = start_date_for_weekly + week

f.close()

