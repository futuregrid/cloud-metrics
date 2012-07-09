#!/usr//bin/env python
# -*- coding: UTF-8 -*-

# FGHighcharts.py (python)
# ------------------------
import re

from futuregrid.cloud.metric.FGUtility import FGUtility

class FGHighcharts:

    chart_type = ""
    res_txt = ""
    filename = ""
    filepath = ""

    title = ""
    subtitle = ""
    xAxis_label = []
    yAxis_title = ""
    data = None
    data_name = None

    def __init__(self, chart_type=""):
        self.chart_type = chart_type

    def set_type(self, name):
        self.chart_type = name

    def set_data(self, data):
        self.data = data
        if type(data) == type({}):
            self.data = self.convert_dict_to_list(data)
            #self.sort_data()
            self.human_sort_data()

    def get_data(self, index=""):
        if not index == "":
            res = []
            for i in self.data:
                res.append(i[int(index)])
            return res
            
        return self.data
    
    def convert_dict_to_list(self, data):
        dictlist = []
        for key, value in data.iteritems():
            temp = [key,value]
            dictlist.append(temp)
        return dictlist

    def sort_data(self):
        self.data = sorted(self.data, key=lambda key: key)

    def human_sort_data(self):
        key_pat = re.compile( r"^(\D+)(\d+)$" )
        def key( item ):
            item = item[0]
            m= key_pat.match( item )
            return m.group(1), int(m.group(2))
        self.data.sort(key=key)

    def set_data_name(self, data_name):
        self.data_name = data_name

    def set_yaxis(self, title):
        self.yAxis_title = title

    def set_xaxis(self, label):
        self.xAxis_categories = label

    def set_output_path(self, path):
        FGUtility.ensure_dir(path + "/" + self.filename)
        self.filepath = path

    def set_filename(self, filename):
        self.filename = filename

    def set_title(self, title):
        self.title = title

    def set_subtitle(self, subtitle):
        self.subtitle = subtitle

    def set_tooltip(self, tooltip):
        if self.chart_type == "pie":
            self.tooltip = "'<b>'+ this.point.name +'</b>: '+ this.y"
        else:
            self.tooltip = "this.x +': '+ this.y"

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
                                %(xAxis_categories)s
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
                                %(tooltip)s;
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
                                type: '%(chart_type)s',
                                name: '%(data_name)s',
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
