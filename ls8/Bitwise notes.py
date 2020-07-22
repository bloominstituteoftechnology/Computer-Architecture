Bitwise Operations
------------------

Truth Table

Boolean:

A   B       A and B
-------------------
F   F         F
F   T         F
T   F         F
T   T         T

if a > 10 and a < 20:
    do something

Bitwise:

A   not A (the bitwise NOT operator is ~)
---------
0     1
1     0

A   B       A xor B  (the bitwise Exclusive-OR operator is ^)
-------------------
0   0         0
0   1         1
1   0         1
1   1         0

A   B       A or B  (the bitwise OR operator is |)
-------------------
0   0         0
0   1         1
1   0         1
1   1         1

A   B       A and B  (the bitwise AND operator is &)
-------------------
0   0         0
0   1         0
1   0         0
1   1         1

NAND == NOT AND
a NAND b == ~(a & b)

NOR == NOT OR
a NOR b == ~(a | b)

Bonus puzzle: if you have only NAND, how can you build NOT?

       vvvv
  0b11101010
& 0b00011110  AND mask
------------
  0b00001010
       ^^^^
    

If an instruction has 2 arguments, the total length is 3 bytes

If an instruction has 1 argument, the total length is 2 bytes

If an instruction has 0 arguments, the total length is 1 byte


To extract bits

1) Mask

    vv
  0b10000010
& 0b11000000
------------
  0b10000000
    ^^

2) Shift   shift operator is >> for right shift, and << for left shift

vv
10000000
01000000
00100000
00010000
00001000
00000100
00000010
      ^^

number of operands = (instruction value & 0b11000000) >> 6
Instruction length = number of operands + 1


Analogy in decimal: extract the number 34 from this number:

  vv
123456

1) Mask

123456
009900
------
003400

2) Shift

003400
000340
000034


Clearing bits

      v
  0b11100011
& 0b11011111   And with 0
------------
  0b11000011


Setting bits

        v
  0b11100011
| 0b00001000   Or with 1
------------
  0b11101011

