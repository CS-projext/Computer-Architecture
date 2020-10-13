#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

program = []
if len(sys.argv) > 1:
  file_name = sys.argv[1]
else:
  file_name = input("Run: ")

f = open(f"examples/{file_name}", "r")
for line in f.readlines():
  if line[0] == "1" or line[0] == "0":
    line_code = line[:8]
    program.append(int(line_code, 2))
f.close()

cpu.load(program)
cpu.run()