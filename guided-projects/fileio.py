#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
    print("usage: fileio.py <filename>", file=sys.stderr)
    sys.exit(1)


try:
    with open(sys.argv[1]) as f:
        for line in f:
            # process comments: ignore anything after a #
            comment_split = [x for x in line.split("#") if x!='']


            #convert numbers from strings binary to integers.


            try:
                num = comment_split[0].strip()
                x = int(num, 2)
            except ValueError as e:
                print(f"WARNING: {e}")
                continue
            except IndexError as e:
                print(f"WARNING: {e}")
                continue

            print(f"{x:08b}: {x}")
except FileNotFoundError:
    print(f"{sys.argv[0]}: {sys.argv[1]} not found")
