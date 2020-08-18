Operation          Boolean Operator         Bitwise Operator
AND                      &&                         &
OR                       ||                         |
XOR                      --                         ^
NOT                       !                         ~


 0b10000011
&0b01010101
------------
 0b00000001

 0b00110101
&0b10101010
------------
 0b00100000

OR
a=True
b=False
(a||b)==True

 0b10101110
|0b11010001
------------
 0b11111111

 0b00101110
|0b10100110
------------
 0b10101110

XOR
'Exclusive or There can only be one'
#Returns true ONLY if 1 of the values is true
a = True
b = False
(a xor b)==True

a=True
b=True
(a xor b)==False

 0b10101101
^0b00110110
------------
 0b10011011

 NOT

 ~0b10101010
 ------------
  0b01010101



  0b10101010
& 0b00000011
--------------
  0b00000010

1. Move them to the side
  -Rightshift the first nibble
2. Mask out the other Bits
  -Mask out the other two

0b10101010 >> 4

 0b00001010
&0b00000011
------------
 0b00000010


#Apply all this to extract instruction length aka num operands
 ADD = 0b10100000
 num_operands = ADD>>6
 is_alu_operation = (ADD>>5)&0b1

 pc+=num_operands + 1

 0b10100000>>5
 0b101 & 0b001--> 0b1