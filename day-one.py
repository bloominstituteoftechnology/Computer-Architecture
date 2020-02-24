'''
0000 0000
4123
4 thousands
1 hundred
2 tens
3 ones
4000 + 100 + 20 + 3
4 * 10^3
1 * 10^2
2 * 10^1
3 * 10^0
0b1010
1 * 2^3
0 * 2^2
1 * 2^1
0 * 2^0
1 * 8
0 * 4
1 * 2
0 * 1
8 + 2 = 10
   8 4 2 1
0b 0 1 1 0
0b00101010
128 + 64 + 32 + 16 + 8 + 4 + 2 + 1
'''

str = "10101010"
def to_decimal(num_string):
    digit_list = list(num_string)
    base = 2
    digit_list.reverse()
    value = 0
    for i in range(len(digit_list)):
        print(f"+({int(digit_list[i])}) * {base ** i}")
        value += int(digit_list[i]) * base ** i
    return value
to_decimal(str)

'''
42 - 32 => 10 - 8 => 2
32 + 8 + 2
0b00101010
198 - 128 => 70 - 64 => 6 - 4 => 2
128 + 64 + 4 + 2
0b11000110
0b10000101
0b1111 1110
0-15
0,1,2,3,4,5,6,7,8,9, A=10, B=11, C=12, D=13, E=14, F=15
0 0000
1 0001
2 0010
3 0011
4 0100
5 0101
6 0110
7 0111
8 1000
9 1001
A 1010
B 1011
C 1100
D 1101
E 1110
F 1111
0b 1000 0101
0x85
0b 1100 0110
0xC6
0x6C = 0b01101100
'''