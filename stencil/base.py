import os
import optparse
import sys
from .resources import Directory, File, Template


class WrongSource(Exception):
    pass


class Stencil(object):

    source = None
    variables = []

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

    def fill_context(self, options):
        for variable in self.variables:
            value = getattr(options, variable.name, None)
            if value is not None:
                self.context[variable.name] = value
            elif variable.name not in self.context:
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

    def get_parser(self):
        option_list = [variable.as_option() for variable in self.variables]
        parser = optparse.OptionParser(option_list=option_list)
        return parser

    @classmethod
    def run(cls, args):
        stencil = cls()
        parser = stencil.get_parser()
        options, args = parser.parse_args(args)
        if len(args) != 1:
            parser.error("target isn't specified.")
        target = os.path.abspath(args[0])
        stencil.fill_context(options)
        stencil.collect_resources()
        stencil.copy(target)
