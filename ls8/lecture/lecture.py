# Number Bases
# Base 2 - binary 0, 1
# Base 8 - octal 0-7
# Base 10 - decimal 0-9
# Base 16 - hexadecimal 0-9,A-F
# Base 64 - Base 64 (64 digits to use): 0-9, A-Z, a-z, +, /

# counting and places
# decimal, base 10
10^0 = 1
10^1 = 10
10^2 = 100
10^3 = 1000
105 = 1 * 10^2 + 0 * 10^1 +  5 * 10^0

# conversions
# binary, base 2:
100101 = 1 * 2^5 + 1* 2^2 + 1 * 2^0 = 37 decimal

# Byte = a number with 8 binary digits ("binary digit" == "bit")
11111111 = 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1= 255 decimal

#from binary to hex:
0b0000 == 0x0
0b0011 == 0x3
0b1111 == 0xF
F is the last digit of hex, so 4 bits == 1 hex digits, so convert by 4 bits 
0b1001011100101101
0b 1001 0111 0010 1101
0x    9    7    2    D 
0x972D

#from decimal to binary:
77 = 64 + 8 + 4 + 1 = 0b1001101

# from hex to binary
0x123ABC
0x 1 2 3 A B C
0b 0001 0010 0011 1010 1011 1100

s = '1000'
print(int(s, 10))
print(int(s, 2))

bin(12345)
a = 0b1000  # binary
a = 0x1000  # hexadecimal
print(bin(a))
print(hex(a))
