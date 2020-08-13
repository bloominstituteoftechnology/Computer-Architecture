'''
Bitwise Operations
-------------------
Boolean:
    and or   True False
    &&  || (Javascript)

octet == byte

A    B    A BITWISE-AND B
--------------------------
0    0         0 (FALSE)
0    1         0 (FALSE)
1    0         0 (FALSE)
1    1         1 (FALSE)


Bitwise Operators:
and: &
or: |
not: ~
xor: ^
shift right: >> - divide by the base
shift left: << - multiply by the base

AND:
  10100100
& 10110111
-----------
  10100100

    vv
  10100100
& 00110000 "AND mask"  - anywhere is a 0 - turns off bit. anywhere is a 1 - turns on bit
-----------
  00100000
    ^^
00100000
00010000
00001000
00000100
00000010 <<  Example of shifting

(0b00100000 & 00110000) >> 4

OR:
  00010001
| 00000100
-----------
  00010101

LDI code for LS-8:
LDI 10000010
LDI R2, 37
10000010 # LDI
00000010 # R2 - register 2
00101001 # 37 - # to be placed in R2

pc += 3

       vv 
ir - 0b100000010 #LDI instruction

  10000010
& 11000000 # mask
-----------
  10000000 # shift
  01000000 # shift
  00100000 # shift
  ..
  00000010 # final result
        ^^

inst_len = ((ir & 11000000)>>6) +1
            ^ inst
                    ^ mask
                            ^ # of spaces needed to shift
                                  ^ + 1 to move pc to next instruction


'''