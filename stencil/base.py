import os
import optparse
import sys
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

    def get_absolute_source_path(self):
        module_path = sys.modules[self.__class__.__module__].__file__
        source_path = os.path.join(os.path.dirname(module_path), self.source)
        return os.path.abspath(source_path)

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
        source_path = self.get_absolute_source_path()
        if not os.path.isdir(source_path):
            raise WrongSource('%s is not a directory' % source_path)
        directories, files, templates = [], [], []
        for path, dirnames, filenames in os.walk(source_path):
            path = os.path.relpath(path, source_path)
            directories.append(Directory(source_path, path))
            for filename in filenames:
                if filename.endswith('_tmpl'):
                    template_path = os.path.join(path, filename)
                    templates.append(Template(source_path, template_path))
                else:
                    files.append(File(source_path, os.path.join(path, filename)))
        self.resources = directories + files + templates

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
