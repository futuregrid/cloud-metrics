Stand Allone Web Server
------------------------------

Often it is convenient to test some features of the metrics framework. If you do not have access to a preinstalled web server, we offer you to use lighttpd. 

Instalation of lighttpd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All you need to do is to insall lighttpd in your machine and make sure you have it in your path.

Using the Standalone server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure you download the code from github.

Generate the code and install it on your system with::

    make force

Than go into the lighttpd directory and say::

   cd lighttpd
   make start

If you like to sop the server say::

  make stop

Browsing the contents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To browse the contents of the created data, simply open your browser  and type in the address

   http://localhost:3000/index.html

Thats all you need to do, it is that simple.

If you are interested in providing us with a better framework for

* drupal
* web2py

or you want to improve the current lighttpd code, please contact

laszewski@gmail.com



