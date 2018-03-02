"""Pipenv Resolveer.

Usage:
  resolver.py
  resolver.py <packages>... [--verbose] [--pre] [--clear]
  resolver.py (-h | --help)
  resolver.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --clear       Clear the cache.
  --verbose     Display debug information to stderr.
  --pre         Include pre-releases.
"""

import os
import sys
import json

os.environ['PIP_PYTHON_PATH'] = sys.executable

for _dir in ('vendor', 'patched', '..'):
    dirpath = os.path.sep.join([os.path.dirname(__file__), _dir])
    sys.path.insert(0, dirpath)

import pipenv.utils
import pipenv.core


def cleanup_sysargv(argv):

    new = []
    for arg in argv.copy():
        if arg.startswith('-e '):
            new.append(arg)
            del argv[argv.index(arg)]

    return argv[1:], new

def which(*args, **kwargs):
    return sys.executable

def resolve(packages, pre, sources, verbose, clear):
    return pipenv.utils.resolve_deps(packages, which, project=project, pre=pre, sources=sources, clear=clear, verbose=verbose)

if __name__ == '__main__':

    argv, new_packages = cleanup_sysargv(sys.argv)
    from docopt import docopt

    args = docopt(__doc__, argv=argv)

    is_verbose = args['--verbose']
    do_pre = args['--pre']
    do_clear = args['--clear']
    packages = args['<packages>']

    for package in new_packages:
        packages.append(package)

    project = pipenv.core.project

    results = resolve(packages, pre=do_pre, sources=project.sources, verbose=is_verbose, clear=do_clear)
    print('XYZZY')
    if results:
        print(json.dumps(results))
    else:
        print(json.dumps([]))