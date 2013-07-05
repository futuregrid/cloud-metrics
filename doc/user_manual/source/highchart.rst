**********************************************************************
Highchart demo in sphinx
**********************************************************************

.. raw:: html

  <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
  <script src="http://code.jquery.com/ui/1.10.1/jquery-ui.js"></script>
  <script src="http://code.highcharts.com/highcharts.js"></script>
  <script>
  $(document).ready(function() {
      var chart = new Highcharts.Chart({

	  chart: {
	      renderTo: 'container',
	      type: 'bar'
	  },
	  title: {
	      text: 'Fruit Consumption'
	  },
	  xAxis: {
	      categories: ['Apples', 'Bananas', 'Oranges']
	  },
	  yAxis: {
	      title: {
		  text: 'Fruit eaten'
	      }
	  },
	  series: [{
	      name: 'Jane',
	      data: [1, 0, 4]},
	  {
	      name: 'John',
	      data: [5, 7, 3]}],
      });
  });
  </script>
  <div id="container" style="width:100%;"></div>

  <script>
  $(document).ready(function() {
      var chart = new Highcharts.Chart({

	  chart: {
	      renderTo: 'container2',
	      type: 'bar'
	  },
	  title: {
	      text: 'Fruit Consumption'
	  },
	  xAxis: {
	      categories: ['Apples', 'Bananas', 'Oranges']
	  },
	  yAxis: {
	      title: {
		  text: 'Fruit eaten'
	      }
	  },
	  series: [{
	      name: 'Gregor',
	      data: [2, 4, 0]},
	  {
	      name: 'Fugang',
	      data: [3, 1, 7]}],
      });
  });
  </script>
  <div id="container2" style="width:100%;"></div>


