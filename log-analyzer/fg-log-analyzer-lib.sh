# 
# Utility libraries for bash shell
#
# February 1st, 2012
# Hyungro Lee (lee212 at indiana dot edu)
#

# This function checks if the parameter is an integer and returns 0 if it is an integer and 1 if not.

function is_integer() {
    [ "$1" -eq "$1" ] > /dev/null 2>&1
    return $?
}
