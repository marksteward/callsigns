#!/usr/bin/env python
# coding=utf-8
from __future__ import division
import sys

if len(sys.argv) != 2:
    print("Usage: generate_callsigns.py <prefix>")
    sys.exit(1)

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
prefix = sys.argv[1]

for i in range(0, 26 * 26 * 26):
    print('%s%s%s%s' % (prefix, chars[i // 26 // 26 % 26], chars[i // 26 % 26], chars[i % 26]))
