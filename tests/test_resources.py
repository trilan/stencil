import os
from nose.tools import eq_, ok_, raises, with_setup
from stencil.resources import Resource, Directory, File, Template, AlreadyExists


sources = os.path.join(os.path.dirname(__file__), 'sources')
resources = os.path.join(sources, 'resources')
target = os.path.join(os.path.dirname(__file__), 'result')


def test_simple_destination():
    resource = Resource('', 'foo')
    eq_(resource.destination({}), 'foo')


def test_destination_with_variable():
    resource = Resource('', '{foo}')
    eq_(resource.destination({'foo': 'bar'}), 'bar')


def test_template_destination():
    template = Template('', 'foo.bar_tmpl')
    eq_(template.destination({}), 'foo.bar')


def test_repr():
    resource = Resource('', 'foo')
    eq_(repr(resource), '<Resource foo>')


@with_setup(teardown=lambda: os.rmdir(os.path.join(target, 'foo')))
def test_directory_copy():
    directory = Directory('', 'foo')
    directory.copy(target, {})
    ok_(os.path.exists(os.path.join(target, 'foo')))


@with_setup(setup=lambda: os.makedirs(os.path.join(target, 'foo')),
            teardown=lambda: os.rmdir(os.path.join(target, 'foo')))
@raises(AlreadyExists)
def test_directory_copy_if_exists():
    directory = Directory('', 'foo')
    directory.copy(target, {})


@with_setup(teardown=lambda: os.remove(os.path.join(target, 'file.txt')))
def test_file_copy():
    file = File(resources, 'file.txt')
    file.copy(target, {})
    ok_(os.path.exists(os.path.join(target, 'file.txt')))


@with_setup(teardown=lambda: os.remove(os.path.join(target, 'template.txt')))
def test_template_copy():
    template = Template(resources, 'template.txt_tmpl')
    template.copy(target, {'foo': 'bar'})
    ok_(os.path.exists(os.path.join(target, 'template.txt')))
    with open(os.path.join(target, 'template.txt')) as f:
        eq_(f.read(), 'bar\n')
