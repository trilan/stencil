import os
from nose.tools import eq_
from stencil.base import Stencil


sources = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sources'))


class Package(Stencil):

    source = 'sources/package'


def test_stencil_absolute_source_path():
    package = Package()
    absolute_path = package.get_absolute_path(package.source)
    eq_(absolute_path, os.path.join(sources, 'package'))
