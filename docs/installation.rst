More on Installation
====================

To install Diderot one can simply

.. code-block:: console

   $ pip install diderot


We strongly recomend the use of `virtualenv`_ (with `virtualenvwrapper`_) to separate multiple projects environments, Python versions, library versions, etc.

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs.html
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/


Running tests locally
---------------------

If you want to clone `diderot repository`_ and run all the tests, first install all libraries for running it.

.. _diderot repository: http://github.com/icaromedeiros/diderot

.. code-block:: console

   $ mkvirtualenv diderot
   $ make install

For running functional and unit tests:

.. code-block:: console

   $ make test

For running only unit tests\:

.. code-block:: console

   $ make unit

For running only functional tests\:

.. code-block:: console

   $ make functional

For running only acceptance tests\:

.. code-block:: console

   $ make acceptance


Compiling documentation
-----------------------

To create this documentation you must first install the required libraries (such as `sphinx`_) for compiling it into ``HTML`` files.

.. _sphinx: http://sphinx-doc.org/

.. code-block:: console

   $ cd docs
   $ make install

To compile the documentation:

.. code-block:: console

   $ make run

This will compile the documentation and open it in your favorite browser.
To compile the documentation and open in a browser in two steps:

.. code-block:: console

   $ make html
   $ make open

This is useful to check if there is compiling errors before opening the documentation.
