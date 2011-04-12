import os
from nose.tools import eq_
from stencil.base import Stencil


sources = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sources'))


class Package(Stencil):

    source = 'sources/package'


def test_stencil_absolute_source_path():
    eq_(Package().get_absolute_source_path(), os.path.join(sources, 'package'))
