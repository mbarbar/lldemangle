#
# lldemangle.py - demangle C++ names in an LLVM ll file.
# Requires c++filt executable.

import re
import subprocess
import sys

USAGE =\
"""\
Usage: {} [options] llfile outfile

options:
  [none yet]
""".format(sys.argv[0])

# Should work with clang.
MANGLED_NAME_RE = re.compile("_Z[a-zA-Z0-9_]*")

def read_mangled_names(llfile):
    mangled_names = set()

    with open(llfile, "r") as f:
        for line in f.readlines():
            line_mangled_names = re.findall(MANGLED_NAME_RE, line)
            for mangled_name in line_mangled_names:
                mangled_names.add(mangled_name)

    return mangled_names

def demangle_names(mangled_names):
    demangled_names = {}
    for mangled_name in mangled_names:
        if mangled_name in demangled_names.keys():
            continue

        demangled_name = subprocess.check_output(["c++filt", mangled_name])
        demangled_names[mangled_name] = demangled_name.strip()

    return demangled_names

def replace_mangled_names(llfile, outfile, mangle_map):
    with open(llfile, "r") as ll, open(outfile, "w") as of:
        for line in ll.readlines():
            line_mangled_names = re.findall(MANGLED_NAME_RE, line)
            for mangled_name in line_mangled_names:
                line = line.replace(mangled_name, mangle_map[mangled_name])

            of.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)

    llfile  = sys.argv[1]
    outfile = sys.argv[2]

    mangled_names = read_mangled_names(llfile)
    mangle_map = demangle_names(mangled_names)
    replace_mangled_names(llfile, outfile, mangle_map)

