import sys
import optparse
from pkg_resources import iter_entry_points


stencils = {}
for entry_point in iter_entry_points('stencils'):
    stencils[entry_point.name] = entry_point.load()


def print_list(option, opt, value, parser):
    for name in sorted(stencils):
        print(name)
    sys.exit(0)


def run():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--list', action='callback', callback=print_list,
                      help='show available stencils and exit')
    parser.disable_interspersed_args()
    options, args = parser.parse_args()
    if not args:
        parser.error("stencil wasn't specified.")
    name = args.pop(0)
    try:
        stencil = stencils[name]
    except KeyError:
        parser.error("stencil %s wasn't found" % name)
    stencil.run(args)


if __name__ == '__main__':
    run()
