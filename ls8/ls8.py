#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()


if len(sys.argv) != 2:
    print("usage: simple.py <filename>", file=sys.stderr)
    sys.exit(1)

    
filepath = sys.argv[1]

cpu.load(filepath)
cpu.run()