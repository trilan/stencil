import sys


def abort(message):
    print >> sys.stderr, 'Error: %s' % message
    sys.exit(1)
