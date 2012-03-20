<?php
namespace fgchart;

require("fgChartInit.php");
require("gChartPhp/gChartInit.php");

$xaxis = utility::httpReq("xaxis");
$yaxis = utility::httpReq("yaxis");
$s_date = utility::httpReq("s_date");
$e_date = utility::httpReq("e_date");
$legend = utility::httpReq("legend");
$duration = utility::httpReq("duration");
$g_options = utility::httpReq("options");
$g_type = utility::httpReq("type");
$g_title = utility::httpReq("title");

$data = new fgData($s_date, $e_date);
$data->getDatabase();
$data->setDuration($duration);
$legends_array = $data->getUniqElement($legend);

$stackedAreaChart = new fgChart($g_type);
$date_range = $data->getDateRange();
foreach($legends_array as $id) {
	$res = $data->getSelectedData(array("Date", $yaxis), "$legend=$id");
	$dataset_array = array();
	foreach($date_range as $dval)
		$dataset_array[] = isset($res[$dval]) ? $res[$dval][$yaxis] : 0;
	$stackedAreaChart->addDataSet($dataset_array);
}
$stackedAreaChart->setLegend($legends_array);
$stackedAreaChart->addXaxisRange($xaxis, $data->getDateRange());
$stackedAreaChart->setYaxis($yaxis);
$stackedAreaChart->setOptions($g_options);
$stackedAreaChart->setTitle($g_title);
$stackedAreaChart->getChartHtml();
//echo $stackedAreaChart->getUrl();
?>
