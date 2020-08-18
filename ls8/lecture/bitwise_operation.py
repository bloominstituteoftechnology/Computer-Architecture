AND    a & b
OR     a | b
NAND ~(a & b)
NOR  ~(a | b)
XOR    a ^ break


# multi-bit numbers

  111010101
& 100011101
------------
  100010101

  11011010
^ 11100011
------------
  00111001

# Use & to mask out unwanted number

  10101101
& 11100000
-------------
  10100000

# left right shift 
     1111
<<1 11110

    1111
>>1  111