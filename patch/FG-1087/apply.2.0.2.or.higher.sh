#!/bin/sh
#
# This is a script for generating a patch that can be applied to future versions (assuming too much does not change).
#
# Hyungro Lee (lee212@indiana.edu)
# April 05, 2011
#

EUCA_VER="2.0.2"
EUCA_FILENAME="eucalyptus-"$EUCA_VER"-src-offline.tar.gz"
EUCA_URL="http://eucalyptussoftware.com/downloads/releases/"$EUCA_FILENAME

########################################################################
#1. download source
echo "\nDownloading eucalyptus..."
/usr/bin/wget -c $EUCA_URL
if [ $? -ne 0 ]
then
	exit -1
fi

echo "\nWhere do you want to extract the $EUCA_FILENAME? (default : ./)"
read DIRE
if [ -z $DIRE ]
then
	DIRE="./"
fi
########################################################################


########################################################################
#2. untar
/bin/tar xvzf $EUCA_FILENAME -C $DIRE
if [ $? -ne 0 ]
then
	exit -1
fi

########################################################################


########################################################################
#3. Apply patch
PATCH_FILENAME="fg-1087.patch"
ORI_NAME="EucalyptusWebInterface.java"
tmp="FG-1087"
PATCH_URL="https://futuregrid.svn.sourceforge.net/svnroot/futuregrid/core/Eucalyptus/patch/FG-1087/ $tmp"
PATCH_PATH="eucalyptus-$EUCA_VER/clc/modules/www/src/main/java/edu/ucsb/eucalyptus/admin/client/"
PATCH_BUILD_PATH="eucalyptus-$EUCA_VER/clc/modules/www"

#1) download
echo "\nDownloading patch files..."
#/usr/bin/wget --no-check-certificate -c $PATCH_URL$PATCH_FILENAME
svn co $PATCH_URL
if [ $? -ne 0 ]
then
	echo "No svn?\n"
	exit -1
fi

echo "\nCopying patch files..."
#2) copy into source directory
#cp -i $PATCH_FILENAME $DIRE"/"$PATCH_PATH"/"$PATCH_FILENAME
/usr/bin/patch $DIRE"/"$PATCH_PATH"/"$ORI_NAME < $tmp/$PATCH_FILENAME

echo "\nIn order to generate root.war on eucalyptus-$EUCA_VER/clc/modules/www, installation of eucalyptus need to be done first. Read INSTALL."
########################################################################
#4. Generate root.war
#cd $DIRE$PATCH_BUILD_PATH
#/usr/bin/ant build-gwt
#RES=$?
#cd -
########################################################################

if [ $RES -ne 0 ]
then
	echo "\nNew patch not applied"
else
	echo "\nNew patch applied"
fi
