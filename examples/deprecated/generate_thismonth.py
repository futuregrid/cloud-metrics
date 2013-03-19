import datetime
today = datetime.date.today()

name = "thismonth"
template_file = name + ".template"

f = open(template_file, "r")
f_txt = f.read()
this_month = "%02d" % today.month
start_ymd = "%d-%02d-%02d" % (today.year, today.month, 1)
end_ymd = "%d-%02d-%02d" % (today.year, today.month, today.day)
replaced_txt = f_txt % vars()
f2 = open(name + ".txt", "w")
f2.write(replaced_txt)
f2.close()
f.close()
