euca_version=2.0.2.1
python_version=2.7

push:
	git commit -a 
	git push

pull:
	git pull 

install:
	# Version variables needed - 02/29/2012
	# $euca_version
	# $python_version
	sudo easy_install dist/futuregrid.euca.analyzer-${euca_version}dev-py${python_version}.egg 

distall:
	make -f Makefile egg
	make -f Makefile tar
#	make -f Makefile rpm


gitgregor:
	git config --global user.name "Gregor von Laszewski"
	git config --global user.email laszewski@gmail.com

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
	sudo easy_install -m dist/futuregrid.euca.analyzer-${euca_version}dev-py${python_version}.egg 
	rm -rf build dist *.egg-info *~ \#*
