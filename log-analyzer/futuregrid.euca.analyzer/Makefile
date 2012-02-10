push:
	git commit -a --author='Gregor von Laszewski <laszewski@gmail.com>' 
	git push

pull:
	git pull 

install:
	sudo easy_install dist/futuregrid.euca.analyzer-0.1dev-py2.6.egg 

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
