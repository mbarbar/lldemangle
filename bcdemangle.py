#
# bcdemangle.py - demangle C++ names in an LLVM bc file.
# Requires c++filt executable.

import re
import sys

USAGE =\
"""\
Usage: {} [options] bcfile

options:
  [todo] todo
""".format(sys.argv[0])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print USAGE
        sys.exit(1)

    bcfile = sys.argv[1]

