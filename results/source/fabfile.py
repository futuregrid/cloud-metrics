import fabric
from fabric.api import local

def all():
    create_build_dir()

def create_build_dir():
    local("mkdir -p build")
    local("cp -rf ../../doc/* build")
    local("cp conf.py build/source")
    local("cp generate-results.py build/source")
    local("cp results.rst build/source")


def clean():
    local("rm -rf build")
          
    
