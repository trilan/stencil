import os
from optparse import make_option


class Variable(object):

    def __init__(self, name, default=None, environ=None, help=None,
                 metavar=None, prompt=None):
        self.name = name
        if environ:
            self.default = os.environ.get(environ, default)
        else:
            self.default = default
        self.help = help
        self.metavar = metavar
        self.prompt_text = prompt

    def is_valid(self, value):
        return value or self.default is not None

    def prompt(self):
        text = self.prompt_text or self.name.replace('_', ' ').capitalize()
        if self.default:
            text = '{0} [{1}]'.format(text, self.default)
        while True:
            value = raw_input('{0}: '.format(text)).strip()
            if self.is_valid(value):
                return value or self.default


class String(Variable):

    def add_to_parser(self, parser):
        parser.add_argument('--{0}'.format(self.name.replace('_', '-')),
                            action='store', dest=self.name,
                            help=self.help, metavar=self.metavar)
