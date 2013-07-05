.. #Browser check. If IE found, notice message will be displayed. 04/18/2013
.. raw:: html

        <div id="checkbrowser"></div>
        <script type="text/javascript">
	function check_browser(f)
	{
		if (navigator.userAgent.indexOf('Firefox') != -1 && parseFloat(navigator.userAgent.substring(navigator.userAgent.indexOf('Firefox') + 8)) >= 3.6){//Firefox
			//Allow
			}else if (navigator.userAgent.indexOf('Chrome') != -1 && parseFloat(navigator.userAgent.substring(navigator.userAgent.indexOf('Chrome') + 7).split(' ')[0]) >= 15){//Chrome
			//Allow
			}else if(navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Version') != -1 && parseFloat(navigator.userAgent.substring(navigator.userAgent.indexOf('Version') + 8).split(' ')[0]) >= 5){//Safari
			//Allow
			}else{
			document.getElementById(f).innerHTML = "<b>Notice</b><br>" + 
			"This application is <font color=\"red\"><b>not officially supported and tested on Internet Explorer</b></font>. If you detect any issues with your browser, please try a different one, you can use Safari, Chrome and Firefox. " + 
			"We also noticed that in some cases you may run out of memory, or have too little space available.  Please clean your machine accordingly. " + 
			"If you still have issues, please let us know.<br>";
			document.getElementById(f).className = "warning" ;

			// Block
		}
	}

        check_browser('checkbrowser')</script>


Cloud Usage Reports
====================
FutureGrid Cloud Metric provides Cloud Usage reports across all sections of IaaS.

- Period: daily, weekly, monthly, and quarterly
- Cloud (IaaS):
   - india.futuregrid.org: Openstack, Eucalyptus
   - sierra.futuregrid.org: Nimbus
   - hotel.futuregrid.org: Nimbus
   - alamo.futuregrid.org: Nimbus
   - foxtrot.futuregrid.org: Nimbus
- Metric: VM instance count, instance wall time, VM CPU cores, memories, disks, and VM instance count per compute node.

Contents:

.. toctree::
	:maxdepth: 3

	results/all
	results/realtime
	results/thismonth
	results/2013-Q1
	results/2013-03
	results/2013-02
	results/2013-01
	results/2012-Q4
	results/2012-12
	results/2012-11
	results/2012-10
	results/2012-Q3
	results/2012-09
	results/2012-08
	results/2012-07
	results/2012-Q2
	results/2012-06
	results/2012-05
	results/2012-04
	results/2012-Q1
	results/2012-03
	results/2012-02
	results/2012-01
	results/2011-Q4
	results/2011-12
	results/2011-11
