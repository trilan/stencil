import os
import optparse
from .resources import Directory, File, Template


class WrongSource(Exception):
    pass


class Stencil(object):

    variables = []

    def __init__(self):
        self.resources = []
        self.context = {}

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def source(self):
        return 'stencils/%s' % self.name

    def copy(self, destination):
        destination = os.path.abspath(destination)
        for resource in self.resources:
            resource.copy(destination, self.context)

    def fill_context(self, options):
        for variable in self.variables:
            value = getattr(options, variable.name, None)
            if value is not None:
                self.context[variable.name] = value
            elif variable.name not in self.context:
                self.context[variable.name] = variable.prompt()

    def collect_resources(self):
        source = os.path.join(os.path.dirname(__file__), self.source)
        if not os.path.isdir(source):
            raise WrongSource('%s is not a directory' % source)
        directories, files, templates = [], [], []
        for root, dirnames, filenames in os.walk(source):
            path = os.path.relpath(root, source)
            directories.append(Directory(source, path))
            for filename in filenames:
                if filename.endswith('_tmpl'):
                    template_path = os.path.join(path, filename)
                    templates.append(Template(source, template_path))
                else:
                    files.append(File(source, os.path.join(path, filename)))
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
            parser.error("destination isn't specified.")
        stencil.fill_context(options)
        stencil.collect_resources()
        stencil.copy(args[0])
