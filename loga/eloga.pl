#!/usr/bin/perl
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
use strict;
use warnings;

#Set variables
my $title_perl="Log file analyzer for Eucalyptus (ElogA)";
my $END="\n";
use constant DEBUG => 2;

# Descriptions of log files
# Key = filename
# Value = description
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

# Description 
#[Mon Apr 26 22:33:09 2010][024529][EUCADEBUG ] refresh_resources(): node=192.168.1.3 mem=7773/7773 disk=267834/267834 cores=4/4
my %desc_logs = ("refresh_resources(): received data", "mem, disk, and cores show (available)/(max) resources");
$desc_logs{"ncClientCall"} = "This is a node controller call from cluster/handler.c. Please see the source code to analyze.";

#No argument
if ( $#ARGV == -1 )  {
	print $title_perl.$END;
	print "Usage: $0 \"log filename\" \"specific log lines\"".$END;
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

		# Get Year/Month/Day/Hour from the logDate
		@newArr = split(/\s+|:/, $new->{logInfo}->{logDate});
		$new->{logInfo}->{logYear} = $newArr[6];
		$new->{logInfo}->{logMonth} = $newArr[1];
		$new->{logInfo}->{logDay} = sprintf ("%02d",$newArr[2]);
		$new->{logInfo}->{logHour} = $newArr[3];

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
$first->report("RunInstances", $theTime, "hourly");

#Report 'TerminateInstances' data
$first->report("TerminateInstances", $theTime, $output_type);


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
	my ( $self, $func, $time, $out_type) = @_;

	print "[".Util::currentTime()."][DEBUG] Start reporting of $func" .$END if main::DEBUG;
	$self->$func($time, $out_type);
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
	my ( $self, $time, $out_type ) = @_;
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

	my ( $self, $time, $out_type ) = @_;
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
		print "$key: $hash{$key}\n";
	}

	return $self;
}

sub TerminateInstances {

	my ( $self, $time, $out_type ) = @_;
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

		$hash { $hkey } = $hash { $hkey } + 1 if (defined($tmp_val));
		$self = $self->{next};
	}

	foreach $key (sort keys %hash) {
		print "$key: $hash{$key}\n";
	}

	return $self;
}
sub getVal {
	my ( $self, $ref, $key ) = @_;
	my $value = 0;
	my @new_kv = split(/[= ]/, $self->{$ref});

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
	print "logInfo->uId: $self->{logInfo}->{uId}.$END";
	print "logInfo->logType: $self->{logInfo}->{logType}.$END";
	print "msgInfo: $self->{msgInfo}.$END";
	print "first: $self->{first}.$END";
	print "prev: $self->{prev}.$END";
	print "next: $self->{next}.$END";
}

package LogInfo;
sub new
{
	my $class = shift;
	my $self = {
#[Tue Feb  1 00:18:54 2011][009030][EUCADEBUG ]
		logDate => shift,
		logYear => shift,
		logMonth => shift,
		logDay => shift,
		logHour => shift,
		uId => shift,
		logType => shift,
	};
	bless $self, $class;
	return $self;
}

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


#userId=jklingin, emiId=emi-0B951139, kernelId=eki-78EF12D2, ramdiskId=eri-5BB61255, emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml, kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml, ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml, instIdsLen=1, netNamesLen=1, macAddrsLen=1, networkIndexListLen=1, minCount=1, maxCount=1, ownerId=jklingin, reservationId=r-431E081D, keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCSkJh2v6G76slfKVZZ4nsDaDNc+d6grFZL1dqDL9G4VGR9pNd4mFkP75qisw4GFMUfVTPrVYga267yY4d8LMBDZmf/X1mi9O91Isnmzb1bgH2hr8mH4AOjEDOTg1xh6mVTcJ6h98PQfZrg6czJ6tbKNnbkxm84V2AROrVYw3XX5JuxUtF3x4s7lUm7v4WommgXNGPNWHFDYWdUCBM4y+H/N3YCVE1mVKL4KlbX3iX646U6iUeSvZtjRvgrvQEpkXTU9snBGvzZ9dWVpx7wzOxQphDiZ2F9B+/JCAi4k0Dhxj5QcZQTVWr3XhZxTEiIRoXSVlKK7+tT+MNdB0bdCPVF jklingin@eucalyptus, vlan=14, userData=, launchIndex=0, targetNode=UNSET

#$object = new Instance( "jklingin", "emi-0B951139", "eki-78EF12D2");

# PRINT THE HASH
#print %desc_files;

# PRINT THE NEW HASH
#while (($key, $value) = each(%desc_files)){
#	     print $key.", ".$value."\n";
#}

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

sub rtrim($)
{
	my $string = shift;
	$string =~ s/\s+$//;
	return $string;

}
