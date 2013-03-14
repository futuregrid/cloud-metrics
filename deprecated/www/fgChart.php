<?php
namespace fgchart;
require("gChartPhp/gChart.php");
use gchart\gChart;
/**
 * @brief Main class
 *
 * This is the mainframe of the wrapper
 *
 * @version 0.1
 */

class fgChart extends gChart
{
	public $options;
	public $xaxis_label;
	public $xaxis_range;
	public $yaxis_label;
	public $is_stacked;

	public static $googleChartTemplate = "googleChartTemplate.txt";

	/* Chart parameter APIs - http://code.google.com/apis/chart/image/docs/chart_params.html */

	public function __construct($g_type, $width=650, $height=480)
	{
		$this->setChartType($g_type);
		$this->setDimensions($width, $height);
	}
	public function setChartType($type)
	{
		$this->setProperty('cht', $type);
		switch($type) {
		case "stackedArea":
			$this->is_stacked = "true";
			break;
		}
	}
	public function setOptions($val) 
	{
		$this->options = $val;
	}
	public function addXaxisRange($xaxis_label, $xaxis_range) 
	{
		$this->xaxis_label = $xaxis_label;
		$this->xaxis_range = $xaxis_range;
	}
	public function setYaxis($yaxis_label) 
	{
		$this->yaxis_label = $yaxis_label;
	}
	public function getUrl()
	{
		$retStr = parent::getUrl();
		return $retStr;
	}
	private function getLegends()
	{
		return "'".str_replace("|", "', '", urldecode($this->getProperty('chdl')))."'";
	}
	private function getXaxisRange()
	{
		return "'".implode("', '", $this->xaxis_range)."'";
	}
	private function getDataSets()
	{
		return  "[".str_replace("|", "], [", $this->encodeData($this->values,',')) . "]";
	}
	private function getTitle()
	{
		return "'".$this->getProperty('chtt')."'";
	}

	public function getChartHtml() 
	{
		$val = file_get_contents(self::$googleChartTemplate);
		$new_val = str_replace(array("%legends%", "%date_range%", "%data_sets%", "%xaxis%", "%yaxis%", "%title%", "%width%", "%height%",  "%is_stacked%"),
			array($this->getLegends(), $this->getXaxisRange(), $this->getDataSets(), "'".$this->xaxis_label."'", "'".$this->yaxis_label."'", $this->getTitle(), $this->getWidth(), $this->getHeight(), $this->is_stacked),
			$val);

		echo $new_val;
	}
}
