#!/usr/bin/perl
#
# fg.log.analyzer.4.eucalyptus.pl
# ===============================
#
# Log file analyzer for Eucalyptus
# This is a part of the study of Information Services on Cloud Environments
# at Community Grids Lab - Indiana University, Bloomington
#
# Hyungro Lee (lee212@indiana.edu)
# Feb 01, 2011
#
#1. Tell what the log file is ...
#2. Tell what the specific line of the log means ...
#
# exceptions
# - arguments check
# - file exists ?
# - unknown lines?
# - new feature will be added?
#
# Need to 
# - big log files need to be abandoned
# - log cache (.cc.log.eloga) for saving analyzing time
# - mem/disk size of ?
# - default set is ? daily?
#
# Updates made by 12/13/2011
#
# 1. DescribeResources added
#
# - Eucalyptus in debug mode generates monitoring logs every 5secs. The process of monitoring is in order like 
#   1) checking status of nodes
#   2) checking instances in each node
#   "monitor_thread(): running" means checking starts
#   "monitor_thread(): done" means checking's finished
#
# - What we can get from the monitoring log in debug mode
#   1) resource response summary: available instance types of m1.small, c1.medium, m1.large, m1.xlarge, and c1.xlarge
#   2) instance response summary: running status of instances with instanceId, publicIp, and privateIp
#   3) node resource info: available memory, disk, and core from refresh_resources()
#   4) Detailed instance information: reservationId, ts(Start time), ownerId, etc.
#
# - Implementation
#   We will use this analyzing data for 
#   1) real-time monitoring graph report and 
#   2) historical graph (hourly,daily,monthly, and yearly)
#
# - Bugs and questions
#   lee212 at indiana dot edu (Hyungro Lee)
#   

#
# use the right version of the perl lib. This is wrong, TODO
#
use lib qw(/N/u/hrlee/user/lib/perl5
/N/u/hrlee/user/lib/perl5/site_perl);
#
#
# seems date::Parse is not avalable on the real system needs to be fixed on the real system. 
# configuration needs to include the update of the perl distribution
#

use strict;
use warnings;
use Date::Parse;

#Set variables
my $title_perl="Log file analyzer for Eucalyptus (ElogA)";
my $END="\n";
use constant DEBUG => 0;

#No argument
if ( $#ARGV == -1 )  {
	print $title_perl.$END;
	print "Usage: $0 \"log filename\" \"specific log lines\"".$END;
	# gvl: the ip number is not printed like this, must come from a variable
	print "Ex) $0 cc.log or $0 cc.log \"...refresh_resources(): node=192.168.1.3...\"".$END;
	exit;
}

#File read
my $filename = $ARGV[0];
my @raw_data = Util::fileRead($filename);
my $length = @raw_data;

my $first = new Logs();
my $prev_p = $first;
my $line = undef;
my $i = 0;
my @newArr = undef;

#Set Logs objects for cc.log
if ( substr($filename, 0, 6) eq "cc.log" ) {

	print "[".Util::currentTime()."][DEBUG] Set Logs class from the file data" .$END if DEBUG;
	
	for ($i = 0; $i < $length; $i++) 
	{
		# Allocate new Logs object
		my $new = new Logs();
		$line = $raw_data[$i];
		# Parsing each line
		@newArr = split(/[\[\]]/, $line);
			$new->{lineNumber} = $i;
		$new->{rawData} = $line;
		$new->{logInfo}->{logDate} = $newArr[1]; #[Tue Feb  1 00:18:54 2011]
		$new->{logInfo}->{uId} = $newArr[3];
		$new->{logInfo}->{logType} = $newArr[5]; # EUCADEBUG|EUCAINFO|EUCAWARN
		# Setting values with linked list info
		$new->{msgInfo} = $newArr[6]; # newArr[6] is about after 'function_name():'
		$new->{first} = $first;
		$new->{prev} = $prev_p;
		$prev_p->{next} = $new if ($i != 0);

		# Get Year/Month/Day/Hour/Min/Sec from the logDate
		@newArr = split(/\s+|:/, $new->{logInfo}->{logDate});
		$new->{logInfo}->{logYear} = $newArr[6];
		$new->{logInfo}->{logMonth} = $newArr[1];
		$new->{logInfo}->{logDay} = sprintf ("%02d",$newArr[2]);
		$new->{logInfo}->{logHour} = $newArr[3];
		$new->{logInfo}->{logMin} = $newArr[4];
		$new->{logInfo}->{logSec} = $newArr[5];

		if (!$newArr[6] || !$newArr[1] || !$newArr[2] || !$newArr[3] || !$newArr[4] || !$newArr[5])
		{
			print $new->{logInfo}->{logDate}."\n";
			print "$newArr[6] || !$newArr[1] || !$newArr[2] || !$newArr[3] || !$newArr[4] || !$newArr[5]\n";
			exit;
		}

		# Setting the first list values
		$first->copy($new) if ($i == 0);
		$first->{next} = $new if ($i == 1); 

		$prev_p = $new;
		#last if ($i == 400) and DEBUG;
	}
	#$first->printAll();
}

# get current time
my $theTime = Util::currentTime();

# get report type (hourly, daily, weekly, monthly, all)
# idea from awstats
my $output_type = "all"; # (all - default)

#Report 'refresh_resources' data
#$first->report("refresh_resources", $theTime, $output_type);

#Report 'RunInstances' data
#$first->report("RunInstances", $theTime, "hourly");

#Report 'TerminateInstances' data
#:w
#$first->report("TerminateInstances", $theTime, $output_type);

#Report 'DescribeResources(): resource response summary'
#$first->report("DescribeResources", $theTime, "hourly", "resource response summary");

#Report 'print_ccInstance(): refresh_instances():'
#$first->report("print_ccInstance", $theTime, "hourly", "refresh_instances()");
my $s_time = str2time("11/09/2011"); # Return unix timestamp ex. 1320814800
my $e_time = str2time("11/10/2011");

# Generates a report between $s_time and $e_time
$first->report("print_ccInstance", $s_time, $e_time, "daily", "refresh_instances()");

# Note 1 (01/10/2011)
#  Calling report above should be emerged to remove duplicated functions.
#  1. reading cc.log takes too long
#  2. reading lines to make an array of analyzed lines should be done by one time and need to be shared by other functions. $first should have that information
#  3. Anything else?

print "[".Util::currentTime()."][DEBUG] Done" .$END if DEBUG;

#################################################################################

# = uppermost  =
# line number
# raw data
# front info (object)
# msg info (object)
# ; ->func, key=value, mesg, ->type (debug or ...), etc
#not now #next## $list_of_run=addRuninstances($msg);
#not now next## $list_of_ter=addTer...
# $list_of_all

# = new layers =
# $list_of_run->prev,first,next
# list of the objects of runinstances
# list of the objects of terminatesInstances
# ...

package Logs;
sub new
{
	my $class = shift;
	my $self = {
		lineNumber => shift,
		rawData => shift,
		logInfo => new LogInfo(),
		msgInfo => shift,
		first => shift,
		prev => shift,
		next => shift,
	};
	bless $self, $class;
	return $self;
}

sub report {
	my ( $self, $func, $s_time, $e_time, $out_type, $search_msg) = @_;

	print "[".Util::currentTime()."][DEBUG] Start reporting of $func" .$END if main::DEBUG;
	$self->$func($s_time, $e_time, $out_type, $search_msg);
	return $self;
}
# trying to get key=value for manipulating data e.g. summary of resource using per hr/day/week/month
# e.g. what need for refresh_resource
# - function name
# - disk / mem / core / node
# 
# display example
# -- hour report -- (detail) -d option
# Feb 1, 1:00pm, i18, mem=24276/23252, disk=287504/286985, cores=8/7
# Feb 1, 2:00pm, i18, mem=24276/23252, disk=287504/286985, cores=8/7
# ...
# Feb 1, 1:00pm , i19 , mem=
# ...
# (regular - Average) no -d option
# Feb 1, 1:00pm, i1 ~ i19, mem=242760/232520 (95% avail), disk=2875040/2869850 (99%), cores=80/70 (87%)
#
# -- day report -- / week / month are same

sub refresh_resources {
	my ( $self, $time, $out_type, $search_msg ) = @_;
	my $mem_m = 0;
	my $mem_a = 0;
	my $disk_m = 0;
	my $disk_a = 0;
	my $cores_m = 0;
	my $cores_a = 0;
	my $i = 0;
	my @newArr;
	my $new_func = "";
	my $tmp_val = undef;
	my @tmp = undef;
	my $count = 0;

	while ($self) {
		@newArr = split(/[\[\]]/, $self->{rawData}); #
			$new_func = substr($newArr[6], 0, index($newArr[6], ":"));
		if ($new_func ne " refresh_resources()") {
			$self = $self->{next};
			next;
		}
		$tmp_val = $self->getVal("msgInfo", "mem");
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$mem_m += $tmp[0];
			$mem_a += $tmp[1];
		}
		$tmp_val = $self->getVal("msgInfo", "disk");
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$disk_m += $tmp[0];
			$disk_a += $tmp[1];
		}
		$tmp_val = $self->getVal("msgInfo", "cores");
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$cores_m += $tmp[0];
			$cores_a += $tmp[1];
		}

		$count++ if (defined($tmp_val));
		$self = $self->{next};
	}
	print "$count nodes use "
		. "mem: $mem_m/$mem_a (".&Util::restrict_num_decimal_digits(((1 - ($mem_a/$mem_m))*100), 3)."%), "
		. "disk: $disk_m/$disk_a (".&Util::restrict_num_decimal_digits(((1 - ($disk_a/$disk_m))*100), 3)."%), "
		. "cores: $cores_m/$cores_a (".&Util::restrict_num_decimal_digits(((1 - ($cores_a/$cores_m))*100), 3)."%)"
		. $END;
	return $self;
}

sub RunInstances {

	my ( $self, $time, $out_type, $search_msg ) = @_;
	my $newArr;
	my $mem_m = 0;
	my $mem_a = 0;
	my $disk_m = 0;
	my $disk_a = 0;
	my $cores_m = 0;
	my $cores_a = 0;
	my $i = 0;
	my @newArr;
	my $new_func = "";
	my $tmp_val = undef;
	my @tmp = undef;
	my $nodesArr ;
	my %hash;
	my $hkey;
	my $key;

	while ($self) {
		$hkey = $self->{logInfo}->{logYear} . $self->{logInfo}->{logMonth} . $self->{logInfo}->{logDay} . $self->{logInfo}->{logHour};
		if ( !$hash { $hkey } ) {
			$hash { $hkey } = 0;
		}

		if ($self->{logInfo}->{logType} ne "EUCAINFO  ") {
			$self = $self->{next};
			next;
		}

		@newArr = split(/[\[\]]/, $self->{rawData}); #
			$new_func = substr($newArr[6], 0, index($newArr[6], ":"));
		if ($new_func ne " RunInstances()") {
			$self = $self->{next};
			next;
		}
		
		$tmp_val = $self->getVal("msgInfo", "mem");
		if (defined($tmp_val)) {
			$mem_m += $tmp_val;
		}
		$tmp_val = $self->getVal("msgInfo", "disk");
		if (defined($tmp_val)) {
			$disk_m += $tmp_val;
		}
		$tmp_val = $self->getVal("msgInfo", "cores");
		if (defined($tmp_val)) {
			$cores_m += $tmp_val;
		}
		$tmp_val = $self->getVal("msgInfo", "node");
		if (defined($tmp_val)) {
		}

		$hash { $hkey } = $hash { $hkey } + 1 if (defined($tmp_val));
		$self = $self->{next};
	}

	foreach $key (sort keys %hash) {
		print "[RunInstances]$key: $hash{$key}\n";
	}

	return $self;
}

sub TerminateInstances {

	my ( $self, $time, $out_type, $search_msg ) = @_;
	my $newArr;
	my $mem_m = 0;
	my $mem_a = 0;
	my $disk_m = 0;
	my $disk_a = 0;
	my $cores_m = 0;
	my $cores_a = 0;
	my $i = 0;
	my @newArr;
	my $new_func = "";
	my $tmp_val = undef;
	my @tmp = undef;
	my $count = 0;
	my $nodesArr ;
	my %hash;
	my $hkey;
	my $key;

	while ($self) {

		$hkey = $self->{logInfo}->{logYear} . $self->{logInfo}->{logMonth} . $self->{logInfo}->{logDay} . $self->{logInfo}->{logHour};
		if ( !$hash { $hkey } ) {
			$hash { $hkey } = 0;
		}

		@newArr = split(/[\[\]]/, $self->{rawData}); #
			$new_func = substr($newArr[6], 0, index($newArr[6], ":"));
		if ($new_func ne " TerminateInstances()") {
			$self = $self->{next};
			next;
		}
		
		$tmp_val = $self->getVal("msgInfo", "userId");
		if (defined($tmp_val)) {
		}

		# ex. [TerminateInstances]2011Nov1012: 0
		$hash { $hkey } = $hash { $hkey } + 1 if (defined($tmp_val));
		$self = $self->{next};
	}

	foreach $key (sort keys %hash) {
		print "[TerminateInstances]$key: $hash{$key}\n";
	}

	return $self;
}

sub DescribeResources {

	my ( $self, $time, $out_type, $search_msg) = @_;
	my $newArr;
	my $i = 0;
	my @newArr;
	my $new_func = "";
	my $tmp_val = undef;
	my @tmp = undef;
	my $nodesArr ;
	my %hash = ();
	my $hkey;
	my $key;
	my $key2;
	my $function_name = (caller(0))[3];
	while ($self) {

		$hkey = $self->{logInfo}->{logYear} ."-". $self->{logInfo}->{logMonth} ."-". $self->{logInfo}->{logDay} ."T". $self->{logInfo}->{logHour} . ":00:00";
		if ( !$hash{ $hkey } ) {
			
			$hash{ $hkey } = { 
				count => 0,
				m1_small_a => 0,
				m1_small_m => 0,
				c1_medium_a => 0,
				c1_medium_m => 0,
				m1_large_a => 0,
				m1_large_m => 0,
				m1_xlarge_a => 0,
				m1_xlarge_m => 0,
				c1_xlarge_a => 0,
				c1_xlarge_m => 0,
			}
		}

		@newArr = split(/[\[\]]/, $self->{rawData}); #
		$new_func = Util::trim(substr($newArr[6], 0, index($newArr[6], ":")));
		$new_func = substr($new_func, 0, length($new_func)-2);
		if ($function_name !~ /$new_func/) {
			#if ($new_func =~ /DescribeResources/) {
			$self = $self->{next};
			next;
		}
		if ((length($search_msg) != 0) && ($newArr[6] !~ /$search_msg/)) {
			$self = $self->{next};
			next;
		}
		#  DescribeResources(): resource response summary (name{avail/max}): m1.small{166/192} c1.medium{166/192} m1.large{76/94} m1.xlarge{29/47} c1.xlarge{5/23}
		$tmp_val = $self->getVal("msgInfo", "m1.small", "[{}: ]"); # third parameter is optional; regular expression
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$hash{ $hkey }{ 'm1_small_a' } += $tmp[0];
			$hash{ $hkey }{ 'm1_small_m' } += $tmp[1];
		}

		$tmp_val = $self->getVal("msgInfo", "c1.medium", "[{}: ]"); # third parameter is optional; regular expression
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$hash{ $hkey }{ 'c1_medium_a' } += $tmp[0];
			$hash{ $hkey }{ 'c1_medium_m' } += $tmp[1];
		}
		
		$tmp_val = $self->getVal("msgInfo", "m1.large", "[{}: ]"); # third parameter is optional; regular expression
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$hash{ $hkey }{ 'm1_large_a' } += $tmp[0];
			$hash{ $hkey }{ 'm1_large_m' } += $tmp[1];
		}

		$tmp_val = $self->getVal("msgInfo", "m1.xlarge", "[{}: ]"); # third parameter is optional; regular expression
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$hash{ $hkey }{ 'm1_xlarge_a' } += $tmp[0];
			$hash{ $hkey }{ 'm1_xlarge_m' } += $tmp[1];
		}

		$tmp_val = $self->getVal("msgInfo", "c1.xlarge", "[{}: ]"); # third parameter is optional; regular expression
		if (defined($tmp_val)) {
			@tmp = split(/[\/]/, $tmp_val);
			$hash{ $hkey }{ 'c1_xlarge_a' } += $tmp[0];
			$hash{ $hkey }{ 'c1_xlarge_m' } += $tmp[1];
		}

		$hash{ $hkey }{ 'count' } = $hash{ $hkey }{ 'count' } + 1 if (defined($tmp_val));

		$self = $self->{next};
	}

	foreach $key (sort keys %hash) {
		foreach $key2 (sort keys %{$hash{ $key }} ) {
			print "[$new_func][$key][$key2]: $hash{$key}{$key2}\n";
		}
	}

	return $self;
}

sub print_ccInstance {

	my ( $self, $s_time, $e_time, $out_type, $search_msg) = @_;
	my $newArr;
	my $i = 0;
	my @newArr;
	my $new_func = "";
	my $tmp_val = undef;
	my @tmp = undef;
	my $instanceId = "";
	my $nodesArr ;
	my $hash_ref = {};
	my $owners = {};
	my $ownerId_ref;
	my $instanceIds_ref = {};
	my $hkey;
	my $key, my $key2, my $key3;
	my $count = 0;
	my $function_name = (caller(0))[3];
	my $res_ref = {};
	
	#Set start time from log
	$s_time = Date::Parse::str2time($self->{logInfo}->{logDay}."/".$self->{logInfo}->{logMonth}."/".$self->{logInfo}->{logYear});
	$e_time = Date::Parse::str2time($self->{logInfo}->{logDay}."/".$self->{logInfo}->{logMonth}."/".$self->{logInfo}->{logYear}." 23:59:59");

	while ($self) {

		$hkey = $self->{logInfo}->{logYear} ."-". $self->{logInfo}->{logMonth} ."-". $self->{logInfo}->{logDay};# ."T". $self->{logInfo}->{logHour} . ":00:00";
		if ( ! exists($hash_ref -> { $hkey }) ) {
			
			$s_time = Date::Parse::str2time($self->{logInfo}->{logDay}."/".$self->{logInfo}->{logMonth}."/".$self->{logInfo}->{logYear});
			$e_time = Date::Parse::str2time($self->{logInfo}->{logDay}."/".$self->{logInfo}->{logMonth}."/".$self->{logInfo}->{logYear}." 23:59:59");

			$hash_ref -> { $hkey } = { 
				instanceIds => {},
				owners => {},
				sTime => $s_time,
				eTime => $e_time,
				Year => $self->{logInfo}->{logYear},
				Month => $self->{logInfo}->{logMonth},
				Day => $self->{logInfo}->{logDay}
			}
		}
	
		@newArr = split(/[\[\]]/, $self->{rawData}); #
		$new_func = Util::trim(substr($newArr[6], 0, index($newArr[6], ":")));
		$new_func = substr($new_func, 0, length($new_func)-2);
		if ($function_name !~ /$new_func/) {
			#if ($new_func =~ /DescribeResources/) {
			$self = $self->{next};
			next;
		}
		if ((length($search_msg) != 0) && ($newArr[6] !~ /$search_msg/)) {
			$self = $self->{next};
			next;
		}
		#[Wed Nov  9 17:33:04 2011][008128][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-49D80872 reservationId=r-46C90856 emiId=emi-CD38102F kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/jklingin/centos5-6.x86_64.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Extant ts=1320805502 ownerId=jklingin keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCSkJh2v6G76slfKVZZ4nsDaDNc+d6grFZL1dqDL9G4VGR9pNd4mFkP75qisw4GFMUfVTPrVYga267yY4d8LMBDZmf/X1mi9O91Isnmzb1bgH2hr8mH4AOjEDOTg1xh6mVTcJ6h98PQfZrg6czJ6tbKNnbkxm84V2AROrVYw3XX5JuxUtF3x4s7lUm7v4WommgXNGPNWHFDYWdUCBM4y+H/N3YCVE1mVKL4KlbX3iX646U6iUeSvZtjRvgrvQEpkXTU9snBGvzZ9dWVpx7wzOxQphDiZ2F9B+/JCAi4k0Dhxj5QcZQTVWr3XhZxTEiIRoXSVlKK7+tT+MNdB0bdCPVF jklingin@eucalyptus ccnet={privateIp=10.0.5.2 publicIp=149.165.159.134 privateMac=D0:0D:49:D8:08:72 vlan=12 networkIndex=2} ccvm={cores=1 mem=512 disk=5} ncHostIdx=16 serviceTag=http://i18:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={default }
		
		#Hours
		#Hour -> instances
		#	instance -> user
		#                 -> etc
		#     -> instance -> user
		#                 -> etc
		# Array
		# $hash -> $hkey -> $instances -> $instanceIds
		# $instanceid (new array) -> $key:$values ex. ownerid:jklingin

		my $state, my $ts, my $ownerId;
		$instanceId = $self->getVal("msgInfo", "instanceId");
		$state = $self->getVal("msgInfo", "state"); # third parameter is optional; regular expression
		$ts = $self->getVal("msgInfo", "ts");
		$ownerId = $self->getVal("msgInfo", "ownerId");

		if (defined($instanceId) && defined($ownerId)) {
			$hash_ref -> {$hkey} -> { "instanceIds" } -> { $instanceId } -> { "ownerId" } = $ownerId;
		}

		# We assume instanceId is a unique value. Need to find out how it is generated.
		# Ignore Teardown message once it's notified. EUCADEBUG log generates multiple messages.
		if (defined($hash_ref -> { $hkey } -> { "instanceIds" } -> { $instanceId } -> { "state" })) {
			if (($state eq "Teardown") && ($hash_ref -> { $hkey } -> { "instanceIds" } -> { $instanceId } -> { "state" } eq "Teardown")) {
				$self = $self->{next};
				next;
			}
		}

		$hash_ref -> { $hkey } -> { "instanceIds" } -> { $instanceId } -> { "state" } = $state; # Extant, Pending, and Teardown
		$hash_ref -> { $hkey } -> { "instanceIds" } -> { $instanceId } -> { "ts" } = $ts;
		$hash_ref -> { $hkey } -> { "instanceIds" } -> { $instanceId } -> { "ownerId" } = $ownerId;
		$hash_ref -> { $hkey } -> { "instanceIds" } -> { $instanceId } -> { "logDate" } = $self->{logInfo}->{logDate};

		if ($state eq "Teardown") {
			if ($ts < $s_time) {
				$ts = $s_time;
			}
			my $etime = Date::Parse::str2time($self->{logInfo}->{logDate});
			if ($etime > $e_time) {
				$etime = $e_time;
			}
			$hash_ref -> { $hkey } -> { "owners" } -> { $ownerId } -> { "seconds" } += ($etime - $ts);
		}

		$self = $self->{next};
	}

	foreach $key (sort keys %$hash_ref) {
		foreach $key2 (sort keys %{$hash_ref -> { $key } -> { "instanceIds" }} ) {
				# This is getting complicated. We just need to display which user runs how many instances at a specific time period. ex) admin: 10, inca: 2 (09:00pm 01/05/2011)
				$ownerId_ref = $hash_ref -> { $key } -> { "instanceIds" } -> { $key2 } -> { "ownerId" } ;
				$hash_ref -> { $key } -> { "owners" } -> { $ownerId_ref } -> { "count" } += 1;
				$count = $hash_ref -> { $key } -> { "owners" } -> { $ownerId_ref } -> { "count" };
				$hash_ref -> { $key } -> { "owners" } -> { $ownerId_ref } -> { "instanceIds" } [$count-1] = $key2;

				my $state = $hash_ref -> { $key } -> { "instanceIds" } -> { $key2 } -> { "state" };
				my $logDate = $hash_ref -> { $key } -> { "instanceIds" } -> { $key2 } -> { "logDate" };
				my $ownerId = $hash_ref -> { $key } -> { "instanceIds" } -> { $key2 } -> { "ownerId" };
				my $ts = $hash_ref -> { $key } -> { "instanceIds" } -> { $key2 } -> { "ts" };
				if ( $state eq "Extant" ) {
					$s_time =  $hash_ref -> { $key } -> { "sTime" };
					if ($ts < $s_time) {
					$ts = $s_time;
				}

				my $etime = Date::Parse::str2time( $logDate );
				$e_time =  $hash_ref -> { $key } -> { "eTime" };
				if ($etime > $e_time) {
					$etime = $e_time;
				}
				$hash_ref -> { $key } -> { "owners" } -> { $ownerId } -> { "seconds" } += ( $etime - $ts );
			}
		}
	}

	print "Year, Month, Day, ownerId, used minutes, number of running instances, instances\n";
	foreach $key (sort keys %$hash_ref) {
		my $owners = {};
		$owners = $hash_ref -> { $key } -> { "owners" };
		foreach $key2 (sort keys %$owners) {
			print $hash_ref -> { $key } -> { "Year" };
			print ",";
			print sprintf("%02d", Util::month2number($hash_ref -> { $key } -> { "Month" }));
			print ",";
			print $hash_ref -> { $key } -> { "Day" };
			print ",";
			print $key2;
			print ",";
			print int(($owners -> { $key2 } -> { "seconds" } / 60) + 0.5); # Make it minutes from seconds
			print ",";
			print $owners -> { $key2 } -> { "count" };
			print ",";
			for ($i = 0; $owners -> { $key2 } -> { "instanceIds" }[$i] ; $i++) {
				if ($i != 0) {
					print ";";
				}
				print $owners -> { $key2 } -> { "instanceIds" }[$i];
			}
			print "\n";
		}
	}

	return $self;
}

sub getVal {
	my ( $self, $ref, $key, $regex ) = @_;
	
	if ( !$regex ) {
		$regex = "[= ]"; # default regular expression for the type "key=val"
	}
	#
	# Som logic need to check regex is valid
	#
	my @new_kv = split(/$regex/, $self->{$ref});

	if (length($key) == 0) { # blank key means all keys
		my $k, my $n = 0;
		#foreach $k (@new_kv) {
		#	print "[$n][$k]\n";
		#	$n++;
		#}
		return @new_kv; #return array?
	}

	for ($i = 0; defined($new_kv[$i]) ; $i++) {
		if ($new_kv[$i] eq $key) {
			return $new_kv[$i+1];
		}
	}
	return undef;
}

sub copy
{
	my ( $node, $new ) = @_;
	$node->{lineNumber} = $new->{lineNumber};
	$node->{rawData} = $new->{rawData};
	$node->{logInfo} = $new->{logInfo};
	$node->{msgInfo} = $new->{msgInfo};
	$node->{first} = $new->{first};
	$node->{prev} = $new->{prev};
	$node->{next} = $new->{next};
	return $node;
}

sub printAll {
	my ( $self ) = @_;
	while ($self) {
		$self->printData();
		print $END;
		$self = $self->{next};
	}
}

sub printData {
	my ( $self ) = @_;
	print "lineNumber: $self->{lineNumber}.$END";
	print "rawData: $self->{rawData}.$END";
	print "logInfo->logDate: $self->{logInfo}->{logDate}.$END";
	print "logInfo->logYear: $self->{logInfo}->{logYear}.$END";
	print "logInfo->logMonth: $self->{logInfo}->{logMonth}.$END";
	print "logInfo->logDay: $self->{logInfo}->{logDay}.$END";
	print "logInfo->logHour: $self->{logInfo}->{logHour}.$END";
	print "logInfo->logMin: $self->{logInfo}->{logMin}.$END";
	print "logInfo->logSec: $self->{logInfo}->{logSec}.$END";
	print "logInfo->uId: $self->{logInfo}->{uId}.$END";
	print "logInfo->logType: $self->{logInfo}->{logType}.$END";
	print "msgInfo: $self->{msgInfo}.$END";
	print "first: $self->{first}.$END";
	print "prev: $self->{prev}.$END";
	print "next: $self->{next}.$END";
}


# Descriptions of log files
sub printDescriptionFiles {
	my %desc_files = ("cc.log", "cc.log is a cluster controller log file\nnode memory, disk and processors details on the log file\n");
	$desc_files{"nc-stats"} = "nc-stats is a node controller log\nrun/terminate tracking information\n";
	$desc_files{"sc-stats.log"} = "sc-stats.log is a storage controller log file";
	$desc_files{"walrus-stats.log"} = "walrus is a storage service like Amazon S3";
	$desc_files{"axis2c.log"} = "";
	$desc_files{"cloud-cluster.log"} = "";
	$desc_files{"cloud-debug.log"} = "";
	$desc_files{"cloud-error.log"} = "";
	$desc_files{"cloud-exhaust.log"} = "";
	$desc_files{"cloud-output.log"} = "";
	$desc_files{"httpd-cc_error_log"} = "";
	$desc_files{"upgrade.log"} = "";
}

# descriotion of functions of cc.log
sub printDescriotionFunctions {
	#[Mon Apr 26 22:33:09 2010][024529][EUCADEBUG ] refresh_resources(): node=192.168.1.3 mem=7773/7773 disk=267834/267834 cores=4/4
	my %desc_logs = ("refresh_resources(): received data", "mem, disk, and cores show (available)/(max) resources");
	$desc_logs{"ncClientCall"} = "This is a node controller call from cluster/handler.c. Please see the source code to analyze.";
}

#############################################
#
# package LogInfo
# ===============
# 
# This function will parse the front string of log files
# It looks like
#
# "[Tue Feb  1 00:18:54 2011][009030][EUCADEBUG ]"
#
# First bracket has 'DATE'
# Second bracket has 'uid' ; unique id
# Third bracket has 'logtype'
#
#############################################

package LogInfo;
sub new
{
	my $class = shift;
	my $self = {
		logDate => shift,
		logYear => shift,
		logMonth => shift,
		logDay => shift,
		logHour => shift,
		logMin => shift,
		logSec => shift,
		uId => shift,
		logType => shift,
	};
	bless $self, $class;
	return $self;
}

#############################################
#
# package Instance
# ================
#
# This is similar with logInfo package.
# Here is a sample line of Instance information from log files
#
#userId=jklingin, emiId=emi-0B951139, kernelId=eki-78EF12D2, ramdiskId=eri-5BB61255, emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml, kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml, ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml, instIdsLen=1, netNamesLen=1, macAddrsLen=1, networkIndexListLen=1, minCount=1, maxCount=1, ownerId=jklingin, reservationId=r-431E081D, keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCSkJh2v6G76slfKVZZ4nsDaDNc+d6grFZL1dqDL9G4VGR9pNd4mFkP75qisw4GFMUfVTPrVYga267yY4d8LMBDZmf/X1mi9O91Isnmzb1bgH2hr8mH4AOjEDOTg1xh6mVTcJ6h98PQfZrg6czJ6tbKNnbkxm84V2AROrVYw3XX5JuxUtF3x4s7lUm7v4WommgXNGPNWHFDYWdUCBM4y+H/N3YCVE1mVKL4KlbX3iX646U6iUeSvZtjRvgrvQEpkXTU9snBGvzZ9dWVpx7wzOxQphDiZ2F9B+/JCAi4k0Dhxj5QcZQTVWr3XhZxTEiIRoXSVlKK7+tT+MNdB0bdCPVF jklingin@eucalyptus, vlan=14, userData=, launchIndex=0, targetNode=UNSET
#
# It should be delimited by ", "
# and an each key and a value are seperate by "=" 
#
#############################################
package Instance;
sub new
{
	my $class = shift;
	my $self = {
		userId => shift,
		emiId => shift,
		kernelId => shift,
		ramdiskId => shift,
		emiURL => shift,
		kernelURL => shift,
		ramdiskURL => shift,
		instIdsLen => shift,
		netNamesLen => shift,
		macAddrsLen => shift,
		networkIndexListLen => shift,
		minCount => shift,
		ownderId => shift,
		reservationId => shift,
		ketName => shift,
		vlan => shift,
		userData => shift,
		launchIndex => shift,
		targetNode => shift,
	};
	bless $self, $class;
	return $self;
}



#$object = new Instance( "jklingin", "emi-0B951139", "eki-78EF12D2");


# Examples
# RunInstances 
# Date: Monday Jan 31
# Duration: 19:20:00 ~ 19:20:24
# Users: 2 users requested
# Memories: 512 requested
# Disks: 5 requested
# Cores: 1 requsted
# Networks: 2 Public IPs allocated
# Time taken for launching: 5 secs (avg.)

package Util;
sub restrict_num_decimal_digits
{
	my $num=shift;#the number to work on
		my $digs_to_cut=shift;# the number of digits after 
# the decimal point to cut 
#(eg: $digs_to_cut=3 will leave 
# two digits after the decimal point)

		if ($num=~/\d+\.(\d){$digs_to_cut,}/)
		{
# there are $digs_to_cut or 
# more digits after the decimal point
			$num=sprintf("%.".($digs_to_cut-1)."f", $num);
		}
	return $num;
}

sub fileRead {

	my ( $filename ) = @_;
#print "[DEBUG] Read the file $filename".$END if DEBUG;
	open (FILE, "<", $filename) or die $!;
	my @raw_data = <FILE>;
	close (FILE);

	return @raw_data;
}

sub currentTime {

	my @months = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	my @weekDays = qw(Sun Mon Tue Wed Thu Fri Sat Sun);
	(my $second, my $minute, my $hour, my $dayOfMonth, my $month, my $yearOffset, my $dayOfWeek, my $dayOfYear, my $daylightSavings) = localtime();
	my $year = 1900 + $yearOffset;
	$hour = sprintf ("%02d", $hour);
	$minute = sprintf ("%02d", $minute);
	$second = sprintf ("%02d", $second);
	my $theTime = "$weekDays[$dayOfWeek] $months[$month] $dayOfMonth $hour:$minute:$second $year";

	return $theTime;
}
# Perl trim function to remove whitespace from the start and end of the string
sub trim($)
{
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}
# Left trim function to remove leading whitespace
sub ltrim($)
{
	my $string = shift;
	$string =~ s/^\s+//;
	return $string;
}
# Right trim function to remove trailing whitespace
sub rtrim($)
{
	my $string = shift;
	$string =~ s/\s+$//;
	return $string;

}

# Convert month names to number
sub month2number($)
{
	my $string = shift;
	my %mon2num = qw(
			jan 1  feb 2  mar 3  apr 4  may 5  jun 6
			jul 7  aug 8  sep 9  oct 10 nov 11 dec 12
			);

	return $mon2num{ lc substr($string, 0, 3) };
}

