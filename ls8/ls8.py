#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print("usage: 02_fileio2.py filename")
    sys.exit(1)

cpu.load(sys.argv[1])
cpu.run()