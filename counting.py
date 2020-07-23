"""
Base 10 (decimal system)
0
1
2
...
9
when we're out of chars
10
20
30
...
99
100



Symbols in hex (hexadecimal system)
0
...
9
A
B
C
D
E
F
10 OR 0x10 (0x means it's in hexadecimal)
11
12
13
14
15
16
17
18
19
1A
1B
1C
..
1F
20
21
..
2F
..
9F
A0
..
A9
AA
AB
..
AF
B0
..



Binary
0
1
10
11
100
101
111
1000
1001
1011
1111
10000
10001
...



Converting
hex  -> decimal
0x73 -> 115

(7*16) + 3 = 115

0x10
0x20
...
0x70
+3



0x3F -> 3*16+15 -> 63

0x -> hexadecimal
0d -> decimal
0b -> binary



decimal -> hex
54 -> 0x36

54 / 16 = 3.??
54 - 16*3 = 6
0x36


hex -> decimal
0xE3 -> 14*16 + 3 -> 227


binary -> decimal
0b11001010 -> 202
2 + 8 + 64+ 128 = 202


binary -> hex
0b1010 1100 -> 0xAC
(2+8)   (4+8)
  10      12
  A       C
    0xAC

1       #1
11      #3
111     #7
0b1111  #15
0xF     #15   

4^2 = 16

A single digit of binary is called bit
this is a byte


hex -> decimal
0xAC -> 10*16 + 12 -> 172


The easiest way to do it:
binary -> hex -> decimal
0b1111 1111 -> (1+2+4+8) (1+2+4+8) -> (15)(15) -> 0xFF -> 15*16 + 15 => 255


in CSS:
0xff ff ff is white
15red 15blue 15green

0b11111111 -> is the biggest number in binary. you can't go any bigger
0b11111111 -> it's called that this number is full


Another way:
decimal -> binary 
3 -> 11
3/2 = 1, remainder 1
1/2 = 0, remainder 1

4 -> 100
4/2 = 2, remainder 0
2/2 = 1, remainder 0
1/2 = 0, remainder 1

15 -> 1111
15/2 = 7, remainder 1
7/2 = 3, remainder 1
3/2 = 1, remainder 1
1/2 = 0, remainder 1
"""



# programmatic base conversion
num = 1234
print(num)          # 1234
print(hex(1234))    # 0x4d2

print(f'{num:d}')   # 1234
print(f'{num:x}')   # 0x4d2
print(f'{num:X}')   # 4D2
print(f'{num:b}')   # 10011010010

# pyhton thinks strings are written in base 10
# if we want otherwise, we have to specify the base we want 
s = "1010101"
print(int(s))       # 1010101
print(int(s, 2))    # 85

print(int("E3", 16)) # 227