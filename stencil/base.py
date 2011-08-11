import os
import optparse
import sys

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from clint.textui import colored
from clint.textui import puts

from .utils import abort
from .resources import Directory, File, Template


class WrongSource(Exception):
    pass


class Stencil(object):

    source = None
    variables = []
    help = None

    def __init__(self):
        self.resources = {}
        self.context = {}

    def get_file(self, path):
        return File(path)

    def get_directory(self, path):
        return Directory(path)

    def get_template(self, path):
        return Template(path)

    def get_absolute_path(self, source):
        module_path = sys.modules[self.__class__.__module__].__file__
        source_path = os.path.join(os.path.dirname(module_path), source)
        return os.path.abspath(source_path)

    def get_source_list(self):
        if isinstance(self.source, (list, tuple)):
            source_list = list(self.source)
        else:
            source_list = [self.source]
        source_list = [self.get_absolute_path(source) for source in source_list]
        return [path for path in source_list if os.path.isdir(path)]

    def make_target_dir(self, target):
        try:
            os.makedirs(target, 0755)
        except OSError:
            if not os.path.exists(target):
                abort('can not create directory %s' % target)
            if not os.path.isdir(target):
                abort('target %s exists and is not a directory' % target)
            if not os.access(target, os.R_OK | os.W_OK | os.X_OK):
                abort('directory %s has not enough permissions' % target)
            if os.listdir(target):
                abort('directory %s is not empty' % target)

    def copy(self, target):
        self.make_target_dir(target)
        for path in sorted(self.resources):
            puts('    %s %s' % (colored.green('create'), path))
            real_path = os.path.join(target, path.format(**self.context))
            self.resources[path].copy(real_path, self.context)

    def fill_context(self, args):
        for variable in self.variables:
            value = getattr(args, variable.name, None)
            if value is not None:
                self.context[variable.name] = value
            elif variable.name not in self.context:
                if args.use_defaults and variable.default is not None:
                    self.context[variable.name] = variable.default
                else:
                    self.context[variable.name] = variable.prompt()

    def collect_resources(self):
        source_list = self.get_source_list()
        if not source_list:
            raise WrongSource(
                'None of the source directories exists: %r' % source_path)
        resources = {}
        for source in source_list:
            for root, dirnames, filenames in os.walk(source):
                root = os.path.relpath(root, source)
                for dirname in dirnames:
                    path = os.path.normpath(os.path.join(root, dirname))
                    real_path = os.path.join(source, path)
                    resources[path] = self.get_directory(real_path)
                for filename in filenames:
                    path = os.path.normpath(os.path.join(root, filename))
                    real_path = os.path.join(source, path)
                    if path.endswith('_tmpl'):
                        path = path[:-5]
                        get_resource = self.get_template
                    else:
                        get_resource = self.get_file
                    resources[path] = get_resource(real_path)
        self.resources = resources

    @classmethod
    def add_to_subparsers(cls, name, subparsers):
        parser = subparsers.add_parser(name, help=cls.help)
        for variable in cls.variables:
            variable.add_to_parser(parser)
        parser.add_argument('target', type=cls.absolute_path,
                            help='destination directory')
        parser.set_defaults(func=cls.run)

    @classmethod
    def absolute_path(cls, arg):
        return os.path.abspath(arg)

    @classmethod
    def run(cls, args):
        stencil = cls()
        stencil.fill_context(args)
        stencil.collect_resources()
        stencil.copy(args.target)
