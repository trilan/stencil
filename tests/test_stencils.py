import os
from nose.tools import eq_
from stencil.base import Stencil


sources = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sources'))


class Default(Stencil):

    pass


class Package(Stencil):

    source = 'sources/package'


def test_stencil_default_name():
    eq_(Default().name, 'default')


def test_stencil_default_source():
    eq_(Default().source, 'stencils/default')


def test_stencil_location():
    eq_(Package().location(), os.path.join(sources, 'package'))
