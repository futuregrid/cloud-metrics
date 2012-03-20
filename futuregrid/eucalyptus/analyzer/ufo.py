# Create a chart object of 250x100 pixels


def make_csv_file(users, filename, output_dir):

	f = open(output_dir + "/" + filename + ".csv", "w")
	f.write('ownerId, count of used instances, total runtime, min runtime, max runtime, avg runtime\n')
	for uname in users:
		ucount = users[uname]['count']
		usum = users[uname]['sum']
		umin = users[uname]['min']
		umax = users[uname]['max']
		uavg = users[uname]['avg']
		f.write(uname + ', ' + repr(ucount) + ', ' + repr(usum) + ', ' + repr(umin) + ', ' + repr(umax) + ', ' + repr(uavg) + '\n')
	f.close()

def make_google_motion_chart(users, args):

	output_dir = args.output_dir
	filename = output_dir + "/FGGoogleMotionChart." + args.s_date + "-" + args.e_date + ".html"
	output = FGGoogleMotionChart.gmc_display(users, args)
	
	f = open(filename, "w")
	f.write(output)
	f.close()

######################################################################
# CONVERTER 
######################################################################


# make_report
# -----------
# Create report with user's inputs and report types.
#
# args; user command arguments (array)
#       -i input directory
# 	-o output directory (report csv, png types)
# 	-s start date of report (YYYYmmdd)
#	-e end date of report (YYYYmmdd)
# 
# type; options for report type (array)
#	csv (comma separated files)
#	png (image file)
#
def make_report(args, type=["png"]): # (generate htmls, csv)
	
    # This function will perform:
    # 1. Iterate -input directory
    # 2. Do parse_file which satisfies from s_date to e_date, otherwise it will skip.
    # 3. analyze data (calculate_delta)
    # 4. Generate htmls (display)
    # 4.1. Generate csv files (records)
    
    s_date = datetime.strptime(args.s_date, '%Y%m%d')
    e_date = datetime.strptime(args.e_date, '%Y%m%d')
    e_date = datetime.combine(e_date, time(23, 59, 59))
    input_dir = args.input_dir
    output_dir = args.output_dir

    users = {}
    #1.
    for filename in os.listdir(input_dir):
        log_date = filename_todate(filename)
        if log_date < s_date or log_date > e_date:
            continue
        #2.
        parse_file(input_dir + "/" + filename, instances.add, args.linetypes, debug=False, progress=True)
	#3.
    instances.calculate_delta ()
    # WRITE to DB
    #instances.write_to_db()
    instances.calculate_user_stats (users)
    #print pp.pprint(users)

    #4.
    if (type[type.index("png")]):
        display(users, args.s_date+"-"+args.e_date, output_dir)
    #4.1.
    if (type[type.index("csv")]):
        make_csv_file(users, args.s_date+"-"+args.e_date, output_dir)
    if (type[type.index("gmc")]): # GMC ;Google Motion Chart
        make_google_motion_chart(users, args)# args.s_date+"-"+args.e_date, output_dir)

    return
