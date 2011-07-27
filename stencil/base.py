import os
import optparse
import sys

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from .resources import Directory, File, Template


class WrongSource(Exception):
    pass


class Stencil(object):

    source = None
    variables = []
    help = None

    def __init__(self):
        self.resources = []
        self.context = {}

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

    def copy(self, target):
        for resource in self.resources:
            resource.copy(target, self.context)

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
        directories, files = OrderedDict(), OrderedDict()
        for source in source_list:
            for root, _, filenames in os.walk(source):
                root = os.path.relpath(root, source)
                directories[root] = source
                for filename in filenames:
                    files[os.path.join(root, filename)] = source
        self.resources = []
        for path, source in directories.items():
            self.resources.append(Directory(source, path))
        for path, source in files.items():
            if path.endswith('_tmpl'):
                self.resources.append(Template(source, path))
            else:
                self.resources.append(File(source, path))

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
