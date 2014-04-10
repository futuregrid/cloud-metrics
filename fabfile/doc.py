from fabric.api import task, local
import sys

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

@task
def view():
    """view the documentation in a browser"""
    local("{browser} doc/user_manual/build/html/index.html".format(browser=browser))

@task
def html():
    """build the doc locally and view"""
    local("cd doc/user_manual; make html")
    view()


@task
def gh():
    """deploy the documentation on gh-pages"""
    local("rm -f doc/user_manual/source/modules/*")
    local("git checkout gh-pages")
    local("make pages")

@task
def man():
    """deploy the documentation on gh-pages"""
    #TODO: match on "Commands"
    local("cm man | tail -n+21 > doc/user_manual/source/man/man.rst")


