<?
namespace gchart;

require ("gChartInit.php");
$lineChart = new gLineChart(300,300);
$lineChart->addDataSet(array(112,125,66,40));
$lineChart->setLegend(array("first"));
$lineChart->setColors(array("ff3344"));
$lineChart->setVisibleAxes(array('x','y'));
$lineChart->setDataRange(30,130);
$lineChart->addAxisRange(0, 1, 4, 1);
$lineChart->addAxisRange(1, 30, 130);
$lineChart->addLineFill('B','76A4FB',0,0);

?>
	<img src="<?php print $lineChart->getUrl();  ?>" /> <br> line chart using the gLineChart class.

