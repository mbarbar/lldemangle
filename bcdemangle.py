#
# bcdemangle.py - demangle C++ names in an LLVM bc file.
# Requires c++filt executable.

import re
import subprocess
import sys

USAGE =\
"""\
Usage: {} [options] bcfile

options:
  [todo] todo
""".format(sys.argv[0])

# Should work with clang.
MANGLED_NAME_RE = re.compile("_Z[a-zA-Z0-9_]*")

def read_mangled_names(bcfile):
    mangled_names = set()

    with open(bcfile, "r") as f:
        for line in f.readlines():
            line_mangled_names = re.findall(MANGLED_NAME_RE, line)
            for mangled_name in line_mangled_names:
                mangled_names.add(mangled_name)

    return mangled_names

def demangle_names(mangled_names):
    demangled_names = {}
    for mangled_name in mangled_names:
        demangled_name = subprocess.check_output(["c++filt", mangled_name])
        demangled_names[mangled_name] = demangled_name

    return demangled_names

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print USAGE
        sys.exit(1)

    bcfile = sys.argv[1]

    mangled_names = read_mangled_names(bcfile)
    mangle_map = demangle_names(mangled_names)

