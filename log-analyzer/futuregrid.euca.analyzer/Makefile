gitpush:
	git commit --amend --author='Gregor von Laszewski <laszewski@gmail.com>'
	git push

gitup:
	git up 

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
