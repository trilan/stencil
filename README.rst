Stencil
=======

Stencil creates files and directories from templates. It is inspired by Paste
Templates, but Stencil has no dependencies.

Installation
------------

Install Stencil with pip::

    $ pip install Stencil

It will also install argparse for python < 2.7. There is no python 3 support yet.


Usage example
-------------

To create new file or directory of files and subdirectories from <stencil> use::

    $ stencil [global args] <stencil> [stencil args]

For example, using stencil ``new`` you can create a new project containing a new
stencil::

    $ stencil new mystencil

For creating stencils use ``new`` `stencil`_ as example.
All stencils are collected together using entry points from Distribute.

.. _stencil: https://github.com/trilan/stencil/blob/master/stencil/stencils.py
