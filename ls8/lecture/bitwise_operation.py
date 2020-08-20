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

# to mask out IP address

  255.255.255.0
  11111111.11111111.11111111.00000000

  192.168.0.1
  11000000.10101000.00000000.00000001

# bitwise operation
43545 & 23243 = 2569

# left right shift 
     1111
<<1 11110

    1111
>>1  111

#base 10:
#if we want only number 34 from the following number, we can shift it left and right
   vv
123456789
234567890 # shift L
345678900 # shift L
034567890 # shift R
003456789
000345678
...
000000034
       ^^
# another way to do this:
        vv
    123456789
d&  009900000  # first AND
--------------
    003400000 # then shift
    000340000 
    ...
    000000034

