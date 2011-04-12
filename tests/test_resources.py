import os
from nose.tools import eq_, ok_, raises, with_setup
from stencil.resources import Resource, Directory, File, Template, AlreadyExists


sources = os.path.join(os.path.dirname(__file__), 'sources')
resources = os.path.join(sources, 'resources')
destination = os.path.join(os.path.dirname(__file__), 'result')


def test_simple_destination_path():
    resource = Resource('', 'foo')
    eq_(resource.destination_path({}), 'foo')


def test_destination_path_with_variable():
    resource = Resource('', '{foo}')
    eq_(resource.destination_path({'foo': 'bar'}), 'bar')


def test_template_destination_path():
    template = Template('', 'foo.bar_tmpl')
    eq_(template.destination_path({}), 'foo.bar')


def test_repr():
    resource = Resource('', 'foo')
    eq_(repr(resource), '<Resource foo>')


@with_setup(teardown=lambda: os.rmdir(os.path.join(destination, 'foo')))
def test_directory_copy():
    directory = Directory('', 'foo')
    directory.copy(destination, {})
    ok_(os.path.exists(os.path.join(destination, 'foo')))


@with_setup(setup=lambda: os.makedirs(os.path.join(destination, 'foo')),
            teardown=lambda: os.rmdir(os.path.join(destination, 'foo')))
@raises(AlreadyExists)
def test_directory_copy_if_exists():
    directory = Directory('', 'foo')
    directory.copy(destination, {})


@with_setup(teardown=lambda: os.remove(os.path.join(destination, 'file.txt')))
def test_file_copy():
    file = File(resources, 'file.txt')
    file.copy(destination, {})
    ok_(os.path.exists(os.path.join(destination, 'file.txt')))


@with_setup(teardown=lambda: os.remove(os.path.join(destination, 'template.txt')))
def test_template_copy():
    template = Template(resources, 'template.txt_tmpl')
    template.copy(destination, {'foo': 'bar'})
    ok_(os.path.exists(os.path.join(destination, 'template.txt')))
    with open(os.path.join(destination, 'template.txt')) as f:
        eq_(f.read(), 'bar\n')
