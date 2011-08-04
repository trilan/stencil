import jinja2
import os
from shutil import copyfile


class AlreadyExists(Exception):
    pass


class Resource(object):

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.path)


class Directory(Resource):

    def copy(self, target, context):
        if os.path.exists(target):
            raise AlreadyExists('directory already exists')
        os.makedirs(target, 0755)


class File(Resource):

    def copy(self, target, context):
        copyfile(self.path, target)


class Template(Resource):

    def repr(self, value):
        return repr(value)

    def get_environment(self):
        env = jinja2.Environment()
        env.filters['repr'] = self.repr
        return env

    def get_template(self):
        with open(self.path) as f:
            return self.get_environment().from_string(f.read())

    def render(self, context):
        return self.get_template().render(context)

    def copy(self, target, context):
        with open(target, 'w') as f:
            f.write(self.render(context))
