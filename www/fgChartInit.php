<?php

/**
 * fgChartPhp init script.
 * Sets up include paths based on the directory this file is in.
 * Registers an SPL class autoload function.
 * 
 * Taken from https://github.com/pda/pheanstalk/blob/master/pheanstalk_init.php and modified
 */

$fgChartClassRoot = dirname(__FILE__);
require_once($fgChartClassRoot. '/ClassLoader.php');

fgChart_ClassLoader::register($fgChartClassRoot);
