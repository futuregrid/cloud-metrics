<?php
namespace fgchart;
/**
 * @brief Utility class
 *
 * @version 0.1
 */
class utility 
{
	public static function csv_in_array($url,$delm=";",$encl="\"",$head=false) 
	{ 

		$csvxrow = file($url);   // ---- csv rows to array ----

		$csvxrow[0] = chop($csvxrow[0]); 
		$csvxrow[0] = str_replace($encl,'',$csvxrow[0]); 
		$keydata = explode($delm,$csvxrow[0]); 
		$keynumb = count($keydata); 
		$out = array();

		if ($head === true) { 
			$anzdata = count($csvxrow); 
			$z=0; 
			for($x=1; $x<$anzdata; $x++) { 
				$csvxrow[$x] = chop($csvxrow[$x]); 
				$csvxrow[$x] = str_replace($encl,'',$csvxrow[$x]); 
				$csv_data[$x] = explode($delm,$csvxrow[$x]); 
				$i=0; 
				foreach($keydata as $key) { 
					$out[$z][$key] = $csv_data[$x][$i]; 
					$i++;
				}    
				$z++;
			}
		}
		else { 
			$i=0;
			foreach($csvxrow as $item) { 
				$item = chop($item); 
				$item = str_replace($encl,'',$item); 
				$csv_data = explode($delm,$item); 
				for ($y=0; $y<$keynumb; $y++) { 
					$out[$i][$y] = $csv_data[$y]; 
				}
				$i++;
			}
		}

		return $out; 
	}

	public static function httpReq($key)
	{
		if(isset($_GET[$key]))
			return trim($_GET[$key]);
		else if (isset($_POST[$key]))
			return trim($_POST[$key]);
		return Null;
	}
}
?>
