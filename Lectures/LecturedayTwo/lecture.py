#OPERANDS
a = 0b1001
b = 0b0110

c = a & b #0b0000
d = a | b #0b1111
e = a ^ b # 0b1111
# print(format(c, '04b'))
# print(format(d, '04b'))
# print(format(e, '04b'))


# SHIFTING 
a = 0b1001

b = a << 2 # 100100
print(format(b, '04b'))

c = a >> 2 # 10

print(format(c, '04b'))

# MASKING (selecting parts of binary)

# Meanings of the bits int he first byte of each instruction: 'AABCDDDD'

# * 'AA' number of operands for this opcode, 0-2

INSRUCTION = 0b10000010 # shift >> 6 times --> 0b10 & 0b11 --> 0b10 
PC = 0
number_of_times_to_increment_pc = ((INSRUCTION >> 6) & 0b11) + 1
PC += number_of_times_to_increment_pc






























