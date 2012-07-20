#!/usr//bin/env python
# -*- coding: UTF-8 -*-

# FGHighcharts.py (python)
# ------------------------
import re

from futuregrid.cloud.metric.FGUtility import FGUtility

class FGHighcharts:

    chart_type = ""
    html_header = ""
    html_script = ""
    html_footer = ""
    html_txt = ""
    filename = ""
    filepath = ""

    title = ""
    subtitle = ""
    xAxis_label = []
    yAxis_title = ""
    data = None
    data_name = None
    width = 0
    height = 0

    from_date = None
    f_year = 0
    f_month = 0
    f_day = 0
    to_date = None
    t_year = 0
    t_month = 0
    t_day = 0

    t_month_before = 0

    def __init__(self, chart_type=""):
        self.chart_type = chart_type
        self.width = 400
        self.height = 550

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
    
    def set_from_date(self, date):
        self.from_date = date
        self.f_year = date.year
        self.f_month = date.month - 1
        self.f_day = date.day

    def set_to_date(self, date):
        self.to_date = date
        self.t_year = date.year
        self.t_month = date.month - 1
        self.t_month_before = date.month - 2
        self.t_day = date.day

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

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def display(self):
        
        self.html_txt = self.get_html_header() + self.get_html_script() + self.get_html_footer()
        self.html_txt = self.html_txt % vars(self)

        f = open(self.filepath + "/" + self.filename, "w")
        f.write(self.html_txt)
        f.close()

    def get_html_header(self):
        self.html_header = '''
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <script type='text/javascript' src='../../../../../../../_static/js/jquery-1.7.2.min.js'></script>'''
        return self.html_header

    def get_html_script(self):
        self.html_script = '''
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
                            align: 'right',
                            verticalAlign: 'top',
                            x: -100,
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
        </script>'''

        if self.chart_type == "master-detail":
            self.html_script = '''<script type='text/javascript'>
                //<![CDATA[ 
                $(function () {
                var data = %(data)s ;
                
                var masterChart,
                    detailChart;
                
                $(document).ready(function() {
                
                    // create the master chart
                    function createMaster() {
                        masterChart = new Highcharts.Chart({
                            chart: {
                                renderTo: 'master-container',
                                reflow: false,
                                borderWidth: 0,
                                backgroundColor: null,
                                marginLeft: 50,
                                marginRight: 20,
                                zoomType: 'x',
                                events: {
                
                                    // listen to the selection event on the master chart to update the
                                    // extremes of the detail chart
                                    selection: function(event) {
                                        var extremesObject = event.xAxis[0],
                                            min = extremesObject.min,
                                            max = extremesObject.max,
                                            detailData = [],
                                            xAxis = this.xAxis[0];
                
                                        // reverse engineer the last part of the data
                                        jQuery.each(this.series[0].data, function(i, point) {
                                            if (point.x > min && point.x < max) {
                                                detailData.push({
                                                    x: point.x,
                                                    y: point.y
                                                });
                                            }
                                        });
                
                                        // move the plot bands to reflect the new detail span
                                        xAxis.removePlotBand('mask-before');
                                        xAxis.addPlotBand({
                                            id: 'mask-before',
                                            from: Date.UTC(%(f_year)s, %(f_month)s, %(f_day)s),
                                            to: min,
                                            color: 'rgba(0, 0, 0, 0.2)'
                                        });
                
                                        xAxis.removePlotBand('mask-after');
                                        xAxis.addPlotBand({
                                            id: 'mask-after',
                                            from: max,
                                            to: Date.UTC(%(t_year)s, %(t_month)s, %(t_day)s),
                                            color: 'rgba(0, 0, 0, 0.2)'
                                        });
                
                
                                        detailChart.series[0].setData(detailData);
                
                                        return false;
                                    }
                                }
                            },
                            title: {
                                text: null
                            },
                            xAxis: {
                                type: 'datetime',
                                showLastTickLabel: true,
                                maxZoom: 14 * 24 * 3600000, // fourteen days
                                plotBands: [{
                                    id: 'mask-before',
                                    from: Date.UTC(%(f_year)s, %(f_month)s, %(f_day)s),
                                    to: Date.UTC(%(t_year)s, %(t_month_before)s, %(t_day)s),
                                    color: 'rgba(0, 0, 0, 0.2)'
                                }],
                                title: {
                                    text: null
                                }
                            },
                            yAxis: {
                                gridLineWidth: 0,
                                labels: {
                                    enabled: false
                                },
                                title: {
                                    text: null
                                },
                                min: 0.6,
                                showFirstLabel: false
                            },
                            tooltip: {
                                formatter: function() {
                                    return false;
                                }
                            },
                            legend: {
                                enabled: false
                            },
                            credits: {
                                enabled: false
                            },
                            plotOptions: {
                                series: {
                                    fillColor: {
                                        linearGradient: [0, 0, 0, 70],
                                        stops: [
                                            [0, '#4572A7'],
                                            [1, 'rgba(0,0,0,0)']
                                        ]
                                    },
                                    lineWidth: 1,
                                    marker: {
                                        enabled: false
                                    },
                                    shadow: false,
                                    states: {
                                        hover: {
                                            lineWidth: 1
                                        }
                                    },
                                    enableMouseTracking: false
                                }
                            },
                
                            series: [{
                                type: 'area',
                                name: '%(data_name)s',
                                pointInterval: 24 * 3600 * 1000,
                                pointStart: Date.UTC(%(f_year)s, %(f_month)s, %(f_day)s),
                                data: data
                            }],
                
                            exporting: {
                                enabled: false
                            }
                
                        }, function(masterChart) {
                            createDetail(masterChart)
                        });
                    }
                
                    // create the detail chart
                    function createDetail(masterChart) {
                
                        // prepare the detail chart
                        var detailData = [],
                            detailStart = Date.UTC(%(t_year)s, %(t_month_before)s, %(t_day)s);
                
                        jQuery.each(masterChart.series[0].data, function(i, point) {
                            if (point.x >= detailStart) {
                                detailData.push(point.y);
                            }
                        });
                
                        // create a detail chart referenced by a global variable
                        detailChart = new Highcharts.Chart({
                            chart: {
                                marginBottom: 120,
                                renderTo: 'detail-container',
                                reflow: false,
                                marginLeft: 50,
                                marginRight: 20,
                                style: {
                                    position: 'absolute'
                                }
                            },
                            credits: {
                                enabled: false
                            },
                            title: {
                                text: '%(title)s'
                            },
                            subtitle: {
                                text: '%(subtitle)s'
                            },
                            xAxis: {
                                type: 'datetime'
                            },
                            yAxis: {
                                title: {
                                    text: null
                                },
                                maxZoom: 0.1
                            },
                            tooltip: {
                                formatter: function() {
                                    var point = this.points[0];
                                    return '<b>'+ point.series.name +'</b><br/>'+
                                        Highcharts.dateFormat('%%A %%B %%e %%Y', this.x) + ':<br/>'+
                                        ' ' + Highcharts.numberFormat(point.y, 0) + ' ';
                                },
                                shared: true
                            },
                            legend: {
                                enabled: false
                            },
                            plotOptions: {
                                series: {
                                    marker: {
                                        enabled: false,
                                        states: {
                                            hover: {
                                                enabled: true,
                                                radius: 3
                                            }
                                        }
                                    }
                                }
                            },
                            series: [{
                                name: '%(data_name)s',
                                pointStart: detailStart,
                                pointInterval: 24 * 3600 * 1000,
                                data: detailData
                            }],
                
                            exporting: {
                                enabled: false
                            }
                
                        });
                    }
                
                    // make the container smaller and add a second container for the master chart
                    var $container = $('#container')
                        .css('position', 'relative');
                
                    var $detailContainer = $('<div id="detail-container">')
                        .appendTo($container);
                
                    var $masterContainer = $('<div id="master-container">')
                        .css({ position: 'absolute', top: 300, height: 80, width: '100%%' })
                        .appendTo($container);
                
                    // create master and in its callback, create the detail chart
                    createMaster();
                });
                
            });
                    //]]>  
                    </script>'''

        return self.html_script

    def get_html_footer(self):
        self.html_footer = '''
        </head>
        <body>
        <script src="../../../../../../../_static/js/highcharts.js"></script>
        <script src="../../../../../../../_static/js/modules/exporting.js"></script>
        <div id="container" style="min-width: %(width)spx; height: %(height)spx; margin: 0 auto"></div>
        </body>
        </html>
        ''' 
        return self.html_footer
