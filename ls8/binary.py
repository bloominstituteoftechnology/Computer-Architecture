# bitwise operations
​
# AND (&) 
#  01011010
#& 10101111
#----------
#  00001010
​
# OR ( | )
#  01011010
#| 10101111
#----------
#  11111111
​
# XOR ( ^ )
#  01011010
#| 10101111
#----------
#  11110101
​
# NOT (~)
# 01011010
#---------
# 10100101
​
## SHIFTING
## A << some_number # shift all bits in A by some amount to the left
## B >> some_number # shift all bits in B by some amount to the right
## examples
​
# 0b1110 >> 1 == 0b0111 #(this is the same as dividing by 2)
# 0b1110 << 2 == 0b111000
​
# MASKING ("filtering out certain bits")
#        vv extract these bits 0b01 == 1
x = 0b01001100
# Shift x by 3 to the right
y = x >> 3 # 0b00001001
​
# mask y with 0b00000011
#    0b00000011
#and 0b00001001
# -------------
#    0b00000001
z = y & 0b00000011