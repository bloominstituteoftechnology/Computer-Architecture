'''
BITWISE OPERATIONS
operate on bits 
'''
# These are true or false:

# and 
# && ||
'''
byte = octet is 8 bits so eight ones and zeros
'''
'''
A   B    A BITWISE-AND B
------------------------
0   0         0
0   1         0
1   0         0
1   1         1 
'''
# Bitwise operators
# and: &
# or: |
# not: ~
# xor: ^
# shift right: >>
# shift left: <<






#   10100100
# & 10110111
# ----------
#   10100100

'''
how to ask to print in binary:

           f'{164:b}'
'''
# AND MASK : (or a stencil)
#   vvvv
#   10100100
# & 10110000
# ----------
#   10100000
# true false values could be converted to numbers to compress data


#     vv
#   10100100
# & ????????   v stands for and mask
# ----------
#   00000010

# shift to right:

(0b10100100 & 0b00110000) >> 4

# Decimal:
#   vv
# 123456
# 009900
#-------
# 003400
# extract:
# 000340
# 000034 <<<<< answer

# 1 is the max number in binary, 9 is the max number in dec

"""
LDI 10000010
"""
# LDI R2, 37
# pc += 3

#        vv 
# ir = 0b10000010 LDI


# VV
# 10000010
#&11000000
#---------
# 10000000
# 01000000
# 00100000
# 00010000
# 00001000
# 00000100
# 00000010


# 10000010 <--LDI
# 00000010 <--R2
# 00100101 <-- 37
# 00000000 <-- NOP <--PC jumps here

# inst_len = ((ir & 0b110000000) >> 6) + 1
# pc += inst_len

'''
WITH | you can set bit
'''
#        vvv
#   00010001
# | 00000111
#-----------
#   00010111
'''
AND: clear bits to 0, mask out bits
OR: set bits to 1
SHIFT: with AND to extract sets of bits
'''
