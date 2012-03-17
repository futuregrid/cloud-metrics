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
	public $duration = "monthly"; # daily, weekly, monthly, quarterly, yearly

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
				$csvdata = array_merge($csvdata, $tmp);
			}
		}
		return $csvdata;

	}
	public function getMysqlDatabase() {
	}
	public function getUniqElement($key) {
		foreach($this->data as $k => $v) {
			$res[] = $v[$key];
		}
		$res = array_unique($res);
		return $res;
	}
	public function getSelectedData($fields, $where) {

		$cnt = 0;
		preg_match("/(.+)=(.+)$/",$where, $matches);
		$search_field = $matches[1];
		$search_value = $matches[2];
		$res = array();
		$tmp = array();
		foreach ($this->data as $entry) {
			if($entry[$search_field] == $search_value) {
				foreach ($fields as $field)
					$tmp[$field] = $entry[$field];
				$res[] = $tmp;
			}
			$cnt++;
		}
		$res = $this->convertDataInDuration($res);
		return $res;
	}
	private function convertDataInDuration($data, $duration="") {
		if(!isset($data) || !isset($data[0]['Date']))
			return $data;
		$res = array();
		foreach ($data as $entry) {
			$new_date = $this->getNewDate($entry['Date'], $duration);
			foreach ($entry as $key => $value)
				isset($res[$new_date][$key]) ? $res[$new_date][$key] += $value : $res[$new_date][$key] = $value;
			$res[$new_date]['Date'] = $new_date;
		}
		#return array_merge(array(),$res);
		return $res;
	}
	public function getDateRange($duration="") {
		$res = array();
		if($duration == "")
			$duration = $this->duration;
		for ($c_date = $this->s_date; $c_date <= $this->e_date; $c_date = date("Ymd", strtotime($c_date . " +1 day")))
			$res[] = $this->getNewDate($c_date, $duration);
		$res = array_unique($res);
		sort($res);
		return $res;
	}
	private function getNewDate($date, $duration="") {
		if($duration == "")
			$duration = $this->duration;
		switch(strtolower($duration)) {
		case "daily":
			return date("Ymd", strtotime($date));
			break;
		case "weekly":
			return date("Y\WW", strtotime($date));
			break;
		case "monthly":
			return date("Ym", strtotime($date));
			break;
		case "quarterly":
			return  date("Y", strtotime($date)).ceil(date("m", strtotime($date))/3);
			break;
		case "yearly":
			return date("Y", strtotime($date));
			break;
		}
	}
	public function setDuration($duration) {
		$this->duration = $duration;
	}
}
?>
