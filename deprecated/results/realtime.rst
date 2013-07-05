Real-time data
=======================================

Total VM instances count on FutureGrid
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

	<div style="margin-top:10px;">
	<iframe width="200" height="60" src="/metrics/vmcounter/a.php" frameborder="0"></iframe> instances have been launched since 2010
	</div><br>
- Cloud:
   - India: Openstack, Eucalyptus
   - sierra: Eucalyptus, Nimbus
   - hotel: Nimbus
   - alamo: Nimbus
   - Foxtrot: Nimbus
- Time span:
   - 2011/11/01 is the first date of counting VMs from Eucalyptus
   - 2012/06/01 is the first date of counting VMs from OpenStack
   - 2010/12/16 is the first date of counting VMs from Nimbus

Current running VM instances count (updated every 5 seconds)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

          <script type='text/javascript' src='../_static/js/jquery-1.7.2.min.js'></script>
          
          <link rel="stylesheet" type="text/css" href="/css/normalize.css">
          <link rel="stylesheet" type="text/css" href="/css/result-light.css">
          
          <style type='text/css'>
            
          </style>
          


          <script type='text/javascript'>//<![CDATA[ 
                  function requestData() {
                          $.ajax({
                url: '/metrics/html/results/data/realtime/count_vms_all.php',
                success: function(point) {
                var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is longer than 20
                // add the point
                chart.series[0].addPoint(point[0], true, shift);
                chart.series[1].addPoint(point[1], true, shift);
                //chart.series[2].addPoint(point[2], true, shift);

                // call it again after one second
                setTimeout(requestData, 5000);    

                },
                cache: false
                });
                }
                $(document).ready(function() {
                                Highcharts.setOptions({
                                    global: {
                                        useUTC: false
                                    }
                                });

                                chart = new Highcharts.Chart({
                chart: {
                renderTo: 'container',
                defaultSeriesType: 'spline',
                events: {
                load: requestData
                }
                },
                title: {
                text: 'Live data - Total count of running VMs'
                },
                xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000
                },
                yAxis: {
                minPadding: 1,
                maxPadding: 1,
                title: {
                text: 'Value',
                      margin: 80
                }
                },
                series: [{
                name: '(Eucalyptus on India)',
                      data: []
                        },
                /*{
                name: '(Eucalyptus on Sierra)',
                      data: []
                },*/
                {
                name: '(OpenStack on India)',
                        data: []
                        }

                        ]
                });        
                });
                //]]>  

                </script>
                <script src="../_static/js/highcharts.js"></script>
                <script src="../_static/js/modules/exporting.js"></script>

                <div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>

	Figure 1. Running VMs count for Eucalyptus and OpenStack on India

List of user(s) using VM instances on India
------------------------------------------------------------------

.. raw:: html		

        <script type="text/javascript" src="../_static/js/jquery-1.7.2.min.js"></script>
		<script type="text/javascript" src="../_static/js/jquery.sparkline.js"></script>
		<script type="text/javascript">
			var s_max = 20;
			$(function() {    
				setTimeout(requestData2, 0);
			});
			function requestData2() {
				$.ajax({

					type: 'GET',
					url: '/metrics/html/results/data/realtime/count_vms_users.php?nodename=india',
					dataType: 'json',
					aysync: true,
					success: function(data) {
					var cnt = 0;
					//sortable = [];
					//for (var user in data)
					//	sortable.push([user, data[user]]);
					//sortable.sort(function(a,b) { return a[1] - b[1]} );
						for (i in data) {
							var s_val = "s"+cnt;
							if (eval("typeof "+s_val) == 'undefined') {
								eval("window."+s_val+ " = [];");
							}
							var sl = eval(s_val);
							sl.push(data[i]);
							if (sl.length > s_max)
							sl.splice(0,1);

							if ($('.name'+cnt).length == 0) {
								$("#myList").append("<li><span class=\"name" + cnt + "\"></span><span class=\"value"+cnt+"\"></span><span class=\"dynamicsparkline"+cnt+"\"></span></li>");
							}
							$('.name'+cnt).text(i);
							$('.value'+cnt).text("("+data[i]+")");
							$('.dynamicsparkline'+cnt).sparkline(sl);
							cnt ++;
						}
							
						setTimeout(requestData2, 5000);
					}, cache: false
			}); };
		</script>
	<p>
	<table border=0>
		<tr>
			<td><b>Full Name,</b></td><td><b>Total count of VMs,</b></td><td><b>Sparkline</b></td>
		</tr>   
	</table>

		<ul id="myList"></ul>
        </p>


.. List of user(s) using VM instances on Sierra
.. --------------------------------------------------------------------

.. .. raw:: html

..        <div style="margin-top:10px;">
..	<iframe width="800" height="420" src="data/realtime/count_vms_users_sierra.html" frameborder="0"></iframe>
..	</div>

.. List of user(s) using VM insances on India for Openstack (TBD)
.. ---------------------------------------------------------------
