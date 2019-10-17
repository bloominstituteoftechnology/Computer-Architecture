#!/usr/bin/env python

from math import log, ceil

def bin_to_int(x: str) -> int:
  quantities = [2**k for k,c in enumerate(x)][::-1]

  return sum(int(a)*b for a,b in zip(x, quantities))

def int_to_bin(x: int) -> str:
  N = int(log(x, 2))
  quantities = [2**k for k in range(N)]

  output = str()

  while N>=0:
    if x >= 2**N:
      output += "1"
      x -= 2**N
    else:
      output += "0"
    N -= 1

  return output

def hex_to_int(x: str) -> int:
  hex = {**{f"{k}": k for k in range(10)},
         **{c: k+10 for k, c in enumerate("ABCDEF")}}

  quantities = [16**k for k, _ in enumerate(x)][::-1]

  return sum(hex[a] * b for a,b in zip(x, quantities))

def int_to_hex(x: int) -> str:
  hex = {**{k: f"{k}" for k in range(10)},
         **{k+10: c for k, c in enumerate("ABCDEF")}}
  print(hex)
  N = int(log(x, 16))
  quantities = [16**k for k in range(N)]

  output = str()

  while N>=0:
    n = 16**N

    if x >= n:
      remainder = (x//n) % 16
      output += hex[remainder]
      x -= n
    else:
      output += "0"

    N -= 1
    print(x)
  return output
