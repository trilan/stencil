import sys
import argparse
from pkg_resources import iter_entry_points


stencils = {}
for entry_point in iter_entry_points('stencils'):
    stencils[entry_point.name] = entry_point.load()


def print_list(option, opt, value, parser):
    for name in sorted(stencils):
        print(name)
    sys.exit(0)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--use-defaults', dest='use_defaults',
                        action='store_true', default=False,
                        help="don't ask for variables with defaults if set")
    subparsers = parser.add_subparsers(title='available stencils',
                                       metavar='<stencil>')
    for name, stencil in stencils.items():
        stencil.add_to_subparsers(name, subparsers)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    run()
