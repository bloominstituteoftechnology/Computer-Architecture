# Class II Notes

## Bitwise Operations

```py
# Bitwise Ops
# -----------

# First, Boolean

A  B        A and B
-------------------
F  F           F
F  T           F
T  F           F
T  T           T


A  B        A OR B
-------------------
F  F           F
F  T           T
T  F           T
T  T           T

# Then, bitwise:

A  B        A & B
-------------------
0  0           0
0  1           0
1  0           0
1  1           1


A  B        A | B
-------------------
0  0           0
0  1           1
1  0           1
1  1           1


# Bitwise-AND
    v
    1100
&   0110       "AND masking" (stencil)
--------
    0100
    ^

"""
Bitwise-AND can mask out parts of a number, or clear individual
bits of a number to 0
"""


# Bit Shifting

10101011
01010101
00101010
00010101
00001010
00000101
00000010
00000001
00000000


# Analogy in Base 10 of extracting numbers
# ----------------------------------------

  vv
1234567

0123456     shift 3 right (AKA // 1000)
0012345
0001234
     ^^

0000034 mask out the 34

Now in Binary
-------------
   vvvv
0101001010110
 010100101011
  01010010101
   0101001010
    010100101
     01010010
      0101001
         ^^^^

      0101001
    & 0001111 Mask
    ---------
      0001001
         ^^^^
```

## Bitwise Ops - python
```py

# Right shift operator:
>>

# Left shift operator:
<<
```
