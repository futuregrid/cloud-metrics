#!/usr//bin/env python
# -*- coding: UTF-8 -*-

# FGGoogleMotionChart.py (python)
# -------------------------------
#
# Display google motion chart based on csv data files
# 
# Example of csv file
# -------------------
# filename: user.data.of.eucalyptus.in.india.20110101-20121231.csv
# content:
# name, count, sum, min, avg
# steenoven, 2, 398426.0, 198126.0, 199213.0
# ...
#
# Input (GET/POST)
# ----------------
# metrics
# s_date
# e_date
# title

# https://developers.google.com/chart/interactive/docs/gallery/motionchart
# Note for Developers: Because of Flash security settings, this (and all Flash-based visualizations) might not work correctly when accessed from a file location in the browser (e.g., file:///c:/webhost/myhost/myviz.html) rather than from a web server URL (e.g., http://www.myhost.com/myviz.html). This is typically a testing issue only. You can overcome this issue as described on the Adobe web site.

class GoogleMotionChart:
	def display(self, users, s_date):
		from datetime import date, timedelta, datetime
		
		#Variables
		title = "General%20Utilization%20of%20number%20of%20instances%20of%20eucalyptus%20in%20India"
		gchart_pname = "motionchart"
		gchart_cname = "google.visualization.MotionChart"
		
		cnt = 0
	
		# COLUMNS of REPORT
		column_names = ['ownerid', 'instances'] # When we draw graphs/charts we need to show value names. The first line of csv file has column names but we adjust the names here. This would be removed once we have good column names in csv file.
		column_name0 = column_names[0]
		column_name1 = column_names[1]
		
		# Make tables for the report
		i = 0
		rows = []
		row_size = 0
		s_date = datetime.strptime(s_date, '%Y-%m-%d %H:%M:%S')
		for uname in users:
			rows.append([uname, 'new Date(' + s_date.strftime("%Y") + ',' + s_date.strftime("%m") + ')', str(users[uname]['count'])]) # csv_line[0] = ownerId, csv_line[1] = instances
			row_size = row_size + 1
		
		
		column_size = 3

		ymd = s_date.strftime("%Y") + "-" + s_date.strftime("%m") + "-" + s_date.strftime("%d")
		gchart_options = """ {};
			options['state'] =
			'{\"xZoomedDataMin\":0,\"yAxisOption\":\"2\",\"yZoomedDataMin\":0,\"time\":\"""" + ymd + """\",\"yLambda\":1,\"iconType\":\"VBAR\",\"nonSelectedAlpha\":0.4,\"xZoomedIn\":false,\"showTrails\":false,\"dimensions\":{\"iconDimensions\":[\"dim0\"]},\"yZoomedIn\":false,\"xZoomedDataMax\":19,\"iconKeySettings\":[],\"xLambda\":1,\"colorOption\":\"2\",\"playDuration\":15000,\"xAxisOption\":\"2\",\"sizeOption\":\"_UNISIZE\",\"orderedByY\":false,\"uniColorForNonSelected\":false,\"duration\":{\"timeUnit\":\"D\",\"multiplier\":1},\"yZoomedDataMax\":139,\"orderedByX\":true};';
			options['width'] = 650;
			options['height'] = 480"""
	
		# HTML
		#print metrics
		#print lines
		#print csv_lines
		output = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
		    <title>%(title)s</title>
		      <script type="text/javascript" src="http://www.google.com/jsapi"></script>
		      <script type="text/javascript">
		      google.load('visualization', '1', {packages: ['%(gchart_pname)s']});
		      function drawVisualization() {
				      var data = new google.visualization.DataTable();
				      data.addColumn('string', '%(column_name0)s');
				      data.addColumn('date', 'Date');
					      data.addColumn('number', '%(column_name1)s');
				      data.addRows(["""
		
		i = 0
		output_add = ""
		for row_line in rows:
			if i > 0:
				output_add = output_add + ",\n"
		
			#output_add = output_add + "['" + ('\', \'' . join(map(str, row_line))) + "']"
			output_add = output_add + "['" + row_line[0] + "', " + row_line[1] + ", " + row_line[2] +  "]"
			i = i + 1
		output_add = output_add + "]);"
		
		output = output + output_add
		
		output_add = """
				      var options = %(gchart_options)s;
				      var annotatedtimeline = new %(gchart_cname)s(
					      document.getElementById('visualization'));
				      annotatedtimeline.draw(data, options);
				      }
		
		      google.setOnLoadCallback(drawVisualization);
		      </script>
		      </head>
		      <body style="font-family: Arial;border: 0 none;">
		      <div id="visualization" style="width: 650px; height: 400px;"></div>
		      </body>
		      </html>
		""" 
		output = output + output_add
		
		output = output % vars()
		
		return output
