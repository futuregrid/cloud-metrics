distall:
	make -f Makefile egg
	make -f Makefile tar
#	make -f Makefile rpm

# #####################################################################
# Creating the distribution
# #####################################################################
egg:
	python setup.py bdist_egg

tar:
	python setup.py sdist

rpm:
	python setup.py bdist_rpm


clean:
	sudo rm -r build dist
