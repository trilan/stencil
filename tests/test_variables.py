import os
from nose.tools import eq_, with_setup
from stencil.variables import Variable


def test_default_from_environ():
    os.environ['STENCIL_TEST_VAR'] = 'bar'
    variable = Variable('var', 'foo', 'STENCIL_TEST_VAR')
    eq_(variable.default, 'bar')
    del os.environ['STENCIL_TEST_VAR']


def test_default_if_environ_not_set():
    variable = Variable('var', 'foo', 'STENCIL_TEST_VAR')
    eq_(variable.default, 'foo')
