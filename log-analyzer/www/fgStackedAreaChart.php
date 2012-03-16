<?php
namespace fgchart;

require("fgChartInit.php");

$xaxis = utility::httpReq("xaxis");
$yaxis = utility::httpReq("yaxis");
$s_date = utility::httpReq("s_date");
$e_date = utility::httpReq("e_date");
$legend = utility::httpReq("legend");
$duration = utility::httpReq("duration");
$g_options = utility::httpReq("g_options");
$g_type = utility::httpReq("g_type");
$g_title = utility::httpReq("g_title");

$data = new fgData($s_date, $e_date);
$data->getDatabase();
$stackedAreaChart = new fgChart();
$stackedAreaChart->addDataSet(array(112,315,66,40));
$stackedAreaChart->setLegend(array("first", "second", "third","fourth"));
$stackedAreaChart->addAxisRange(0, 1, 4, 1);
$stackedAreaChart->getChartHtml();

?>
