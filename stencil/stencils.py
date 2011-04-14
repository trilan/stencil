import os

from .base import Stencil
from .variables import String


class New(Stencil):

    source = 'stencils/new'
    help = 'create a project with a new stencil'
    variables = [
        String('name', help='name of the project'),
        String('version', '0.0', help='version of this release'),
        String('description', help='short, summary description of the package'),
        String('author', environ='STENCIL_AUTHOR', help="package author's name"),
        String('author_email', environ='STENCIL_AUTHOR_EMAIL',
               help="package author's email"),
        String('package_name', help='name of the package'),
        String('stencil_name', help='name of the stencil class'),
    ]

    def fill_context(self, args):
        if not args.name:
            self.context['name'] = os.path.basename(args.target)
            for variable in self.variables:
                if variable.name == 'package_name':
                    variable.default = self.context['name'].replace('-', '_')
                    break
        super(New, self).fill_context(args)
        self.context['command_name'] = self.context['stencil_name'].lower()
