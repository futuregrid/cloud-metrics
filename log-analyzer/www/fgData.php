<?php
namespace fgchart;
/**
 * @brief Main class
 *
 * This is the database retrieval
 *
 * @version 0.1
 */
class fgData
{
	public $s_date;
	public $e_date;
	public $ini_array;
	public $data;

	public function __construct($s_date, $e_date) {
		$this->s_date = $s_date;
		$this->e_date = $e_date;
		$this->ini_array = parse_ini_file("futuregrid-www.cfg");

	}
	public function getDatabase() {
		$db_type = $this->ini_array['database'];
		$this->data = $this->{"get".ucfirst($db_type)."Database"}();
	}
	public function getCsvDatabase() {
		$path_to_data4graphs = $this->ini_array['data4graphs'];
		$cnt = 0;
		$csvdata = array();
		for ($c_date = $this->s_date; $c_date <= $this->e_date; $c_date = date("Ymd", strtotime($c_date . " +1 day"))) {
			$yearmonth = substr($c_date, 0, 6);
			$filename = $path_to_data4graphs . "/". $yearmonth . "/" . $c_date . "-" . $c_date . ".csv";
			if( !file_exists($filename))
				continue;
			$res = utility::csv_in_array( $filename , ", ", "", true );
			if (count($res) >= 1) {
				#TEMPORARY LINES FOR DATE PROCESSING ==>
				$date = substr($c_date, 0, 8);
				foreach ($res as $k => $v)
					$tmp[$k] = array_merge($v, array("Date" => $c_date));
				#TEMPORARY LINES DONE <==
				$csvdata = array_merge($tmp, $csvdata);
			}
		}
		return $csvdata;

	}
	public function getMysqlDatabase() {
	}
}
?>
