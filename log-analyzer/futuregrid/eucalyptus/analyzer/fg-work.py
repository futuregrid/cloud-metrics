# WILL BE MERGED WITH fg-parser.py or fg-analyzer.py
	"""
    ---------------------------------------------
	STARTED- H. Lee added
    ---------------------------------------------

class Node(object):
	def __init__(self, data, next=None):
		self.data = data
		self.next = next
		
	def __str__(self):
		return str(self.data)

class LinkedList(object):
	def __init__(self):
		self.head = None
		self.tail = None	
		self.size = 0

	def append(self, data):
		new_node = Node(data)

		if self.tail:
			self.tail.next = new_node
		else:
			# If tail is None, we are adding to an empty list
			self.head = new_node

		self.tail = new_node
		self.size += 1

	def __iter__(self):
		node = self.head
		while node:
			yield node
			node = node.next
		else:
			raise StopIteration


	def __str__(self):
		return ('[' +
				','.join([str(node) for node in self]) +
				']')

    def report(linked_list, function_name, report_period, optional_search_words):

    	# This function will make a csv typed report based on parsed logs.
	#
	# Parameters
	#  linked_list; A linked list of parsed logs
	#  function_name; A name of functions in logs. We assume cc.log is only one that we are parsing here. 
	#  		  So, print_ccInstance, DescribeResources, TerminateInstances, RunInstances, and refresh_resources would be one of the function name.
	#  report_period; 

    	# Report types that we are looking for now.
	  1) minutes used by users
	  2) a number of used instances by users
	  3) ...

	#

	# 1. Read the linked list 
	for i in linked_list:
		
		# 2. Create a new linked list for a result
			- We will use a Date as a key of the new linked list. That would be easy to accumulate values.
			- ex) if key is a date and the sub keys might look like 
				'2012-02-13' -> 'user name or instance ids' -> 'a number of launched/running instances' = 32
			
   
   	

    	# For minutes used by users

	    - what we need
	     1) user name
	     2) start time for currently running instances (*start time is or start time of report whichone comes late) 
	     3) end time - start time for terminated instances (*start time is or start time of report whichone comes late) 
	
	     Add all minutes 2), 3) and set it with user name
	
	#    How to ?
	     - state indicates three types 'Extant', 'Teardown' and 'Pending'
	     - Here comes a flow chart
	    
	    if (instance is died?)
		- Get start time of the instance
		
		if (the start time is older than the start time of the report?)

		(We assume we now have a start time and an end time of the instance
		
		if (
	
	    	- Get time from the last line of logs where the instance's message is included
	    
	    Exceptions ?
	    - log generates duplicated lines. Skipping same line logic needed


    ---------------------------------------------
    	ENDED-
    ---------------------------------------------
	"""


#####################################################################
# MAIN
#
#####################################################################
def main():

	"""
    ---------------------------------------------
	STARTED- H. Lee added
    ---------------------------------------------

    # 1. optparse . Parser for command line options
	- possible options
	- 1) filename
	- 2) function name to parse
	- 3) output filename
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="input_filename",
				      help="input filename FILE", metavar="FILE")
    parser.add_option("-0", "--output", dest="output_filename",
				      help="output filename", metavar="FILE")

    (options, args) = parser.parse_args()

    # 2. READ file contents from options
    #input_filename = "~/tmp/cc.log"
    f = open(input_filename, "r", 0)

    # 3. Iteration for making a linked list of parsed logs
    linked_list = LinkedList()
    for line in f:
	data = ccInstance_parser(line)
	linked_list.append(data)

    # 4. Make a report
    result = report(linked_list, function_name, period (daily, weekly), optional search words)

    # 5. Write file to $output_filename
    result

    ---------------------------------------------
	ENDED-
    ---------------------------------------------
    """
