import os
from shutil import copyfile


class AlreadyExists(Exception):
    pass


class Resource(object):

    def __init__(self, source, path):
        self.source = source
        self.path = path

    def destination_path(self, context):
        return self.path.format(**context)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.path)


class Directory(Resource):

    def copy(self, destination, context):
        destination_path = self.destination_path(context)
        destination = os.path.join(destination, destination_path)
        if os.path.exists(destination):
            if self.path != '.':
                raise AlreadyExists('directory already exists')
        else:
            os.makedirs(destination, 0755)


class File(Resource):

    def copy(self, destination, context):
        destination_path = self.destination_path(context)
        destination = os.path.join(destination, destination_path)
        source = os.path.join(self.source, self.path)
        copyfile(source, destination)


class Template(Resource):

    def destination_path(self, context):
        return super(Template, self).destination_path(context)[:-5]

    def copy(self, destination, context):
        destination_path = self.destination_path(context)
        destination = os.path.join(destination, destination_path)
        source = os.path.join(self.source, self.path)
        with open(source) as f:
            content = f.read()
        with open(destination, 'w') as f:
            f.write(content.format(**context))
