#!/usr/bin/perl
#
# fg-google-line-chart.ph
# =======================
#
# This script generates csv typed data file from an output of log analyzer looks like below.
#
#[DescribeResources][2011-Nov-10T22:00:00][c1_medium_a]: 8550
#[DescribeResources][2011-Nov-10T22:00:00][c1_medium_m]: 9000
#[DescribeResources][2011-Nov-10T22:00:00][c1_xlarge_a]: 630
#[DescribeResources][2011-Nov-10T22:00:00][c1_xlarge_m]: 1080
#[DescribeResources][2011-Nov-10T22:00:00][count]: 45
#[DescribeResources][2011-Nov-10T22:00:00][m1_large_a]: 3915
#[DescribeResources][2011-Nov-10T22:00:00][m1_large_m]: 4365
#[DescribeResources][2011-Nov-10T22:00:00][m1_small_a]: 8550
#[DescribeResources][2011-Nov-10T22:00:00][m1_small_m]: 9000
#[DescribeResources][2011-Nov-10T22:00:00][m1_xlarge_a]: 1710
#[DescribeResources][2011-Nov-10T22:00:00][m1_xlarge_m]: 2160
#
#
# ======================================
# Last updated by 12/11/2011
# Hyungro Lee (lee212 at indiana dot edu)
#

sub trim($);
sub month2number($);

my %hash;
my $i = 0;
my $line = "";
my @tmp = undef;
my @tmp2 = undef;
my $val;
my $date;
my $year;
my $month;
my $day;
my $hour;
my $count = 0;
my %hash = ();

@userinput = <STDIN>;

for ($i = 0; $line = $userinput[$i] ; $i++) {
	@tmp = split(/[\[\]]/, $line);
	$date = $tmp[3];
	@tmp2 = split(/[: ]/, $tmp[6]);
	$hash{$date}{$tmp[5]} = trim($tmp2[2]);
	$year = substr($date, 0, 4);
	$hash{$date}{'year'} = $year;
	$month = month2number(substr($date, 5, 3));
	$hash{$date}{'month'} = $month;
	$day = substr($date, 9, 2);
	$hash{$date}{'day'} = $day;
	$hour = substr($date, 12, 2);
	$hash{$date}{'hour'} = $hour;
}

#print "Year, Month, Day, Hour, c1_medium_a, c1_medium_m, c1_xlarge_a, c1_xlarge_m, m1_large_a, m1_large_m, m1_small_a, m1_small_m, m1_xlarge_a, m1_xlarge_m";
print "Year, Month, Day, Hour, m1_small, c1_medium, m1_large, m1_xlarge, c1_xlarge\n";
foreach my $k (sort keys %hash) {
	foreach my $k2 (sort keys %{$hash{$k}}) {
		#print "$k,$k2: $hash{$k}{$k2}\n";
	}
	print "$hash{$k}{'year'}, $hash{$k}{'month'}, $hash{$k}{'day'}, $hash{$k}{'hour'}, ";
	print int((($hash{$k}{'m1_small_m'} - $hash{$k}{'m1_small_a'}) / $hash{$k}{'count'}) + 0.5);
	print ", ";
	print int((($hash{$k}{'c1_medium_m'} - $hash{$k}{'c1_medium_a'}) / $hash{$k}{'count'}) + 0.5);
	print ", ";
	print int((($hash{$k}{'m1_large_m'} - $hash{$k}{'m1_large_a'}) / $hash{$k}{'count'}) + 0.5);
	print ", ";
	print int((($hash{$k}{'m1_xlarge_m'} - $hash{$k}{'m1_xlarge_a'}) / $hash{$k}{'count'}) + 0.5);
	print ", ";
	print int((($hash{$k}{'c1_xlarge_m'} - $hash{$k}{'c1_xlarge_a'}) / $hash{$k}{'count'}) + 0.5);
	print "\n";
}
#print int(($val/$count)+0.5); # round() function
# Google chart data should look like
#           [new Date(2008, 1 ,1), 30000, undefined, undefined, 40645, undefined, undefined],
#
# We will write data on a file instead of using database now. It should be easy to convert a file data to a database. But it needs 1) installation of mongodb (or else),
# 2) connecting db with api, 3) converting perl scripts to python. - It will be done later once we understand this activity is meaningful to keep then we will go forward to a next step.
#

sub trim($)
{
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}

sub month2number($)
{
	my $string = shift;
	my %mon2num = qw(
	jan 1  feb 2  mar 3  apr 4  may 5  jun 6
	jul 7  aug 8  sep 9  oct 10 nov 11 dec 12
	);
    
	return $mon2num{ lc substr($string, 0, 3) };
}

