#!/usr//bin/env python
# -*- coding: UTF-8 -*-

# FGHighcharts.py (python)
# ------------------------
from futuregrid.cloud.metric.FGUtility import Utility

class Highcharts:

    chart_type = ""
    res_txt = ""
    filename = ""
    filepath = ""

    title = ""
    subtitle = ""
    xAxis_label = []
    yAxis_title = ""
    data = None

    def __init__(self, chart_type):
        self.chart_type = chart_type

    def set_data(self, data):
        self.data = data

    def set_yaxis(self, title):
        self.yAxis_title = title

    def set_xaxis(self, label):
        self.xAxis_label = label

    def set_output_path(self, path):
        Utility.ensure_dir(path + "/" + self.filename)
        self.filepath = path

    def set_filename(self, filename):
        self.filename = filename

    def set_title(self, title):
        self.title = title

    def set_subtitle(self, subtitle):
        self.subtitle = subtitle

    def display(self):
        
        self.res_txt = '''
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <script type='text/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js'></script>
        <link rel="stylesheet" type="text/css" href="/css/normalize.css">
        <link rel="stylesheet" type="text/css" href="/css/result-light.css">
        <script type='text/javascript'>
        //<![CDATA[ 
            $(function () {
                var chart;
                $(document).ready(function() {
                    chart = new Highcharts.Chart({
                        chart: {
                            renderTo: 'container',
                            type: 'column'
                            },
                        title: {
                            text: '%(title)s'
                            },
                        subtitle: {
                            text: '%(subtitle)s'
                            },
                        xAxis: {
                            categories: 
                                %(xAxis_label)s
                            },
                        yAxis: {
                            min: 0,
                            title: {
                                text: '%(yAxis_title)s'
                                }
                            },
                        legend: {
                            layout: 'vertical',
                            backgroundColor: '#FFFFFF',
                            align: 'left',
                            verticalAlign: 'top',
                            x: 100,
                            y: 70,
                            floating: true,
                            shadow: true
                            },
                        tooltip: {
                            formatter: function() {
                                return ''+
                                this.x +': '+ this.y;
                                }
                            },
                        plotOptions: {
                            column: {
                                pointPadding: 0.2,
                                borderWidth: 0
                                }
                            },
                        series: [
                            {
                                data: %(data)s
                            }]
                        });
                    });
            });
        //]]>  
        </script>
        </head>
        <body>
        <script src="http://code.highcharts.com/highcharts.js"></script>
        <script src="http://code.highcharts.com/modules/exporting.js"></script>
        <div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>
        </body>
        </html>
        ''' % vars(self)

        f = open(self.filepath + "/" + self.filename, "w")
        f.write(self.res_txt)
        f.close()
