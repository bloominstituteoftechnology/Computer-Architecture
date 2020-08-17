Why different number bases?
Hexadecimal
- easier to write large numbers
Binary
- translate electricity into data
- ternary computer 
- plays well with Boolean logic
Arithmetic for Billy Goats
Base 12 for time
Octal
Place-based number systems
I, II, III, IV, V, VI
XLVII
CXC
"Logicomix" - Bertrand Russell
0
1
2
3
4
5
6
7
8
9
10
19
20
 99
100
Counting in Hex
Hexadecimal
0
1
2
3
4
5
6
7
8
9
A
B
C
D
E
F
10
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
1D
1E
1F
20
Conversions Hex <-> Decimal
0x20 --> decimal
(2 * 16) + 0 = 32
0x73
(7 * 16) + 3 --> 112 + 3 = 115
0x5E --> decimal
(5 * 16) + 14 = 80 + 14 = 94
95 --> hex
95/16 --> 0x5F
53 --> hex
53/16 --> 3, then a remainder
0x35
Counting in Binary
0
1
10
11
100
101
110
111
1000
1001
1010
1011
1100
1101
1110
1111
base 10 (decimal)
+-----1000's place
|+----100's place
||+---10's place
|||+--1's place
||||
abcd
1234
1 * 1000 + 2 * 100 + 3 * 10 + 4 * 1 == 1234
base 2 (binary)
+-----8's place (0b1000's place)
|+----4's place (0b100's place)
||+---2's place (0b10's place)
|||+--1's place (0b1's place)
||||
abcd
1110 (binary)
1 * 8 + 1 * 4 + 1 * 2 + 0 * 1 = 14
000000001001
25 --> binary
0b11001
1001010 --> decimal
64 + 8 + 2 = 74
47 --> Binary
00101111
128 64 32 16 8 4 2 1
0    0  1  0 1 1 1 1
8 bits --> byte
0b00000000
Math is the same
0b1010
0b0000 0000
0b1111 --> decimal?
15
in hex, what is the largest number with a single number?
0...F
F --> 15
0b1111 1111 --> hex
    F   F
    0xFF
in decimal, this is...255
(15 * 16) + 15
Binary    Hex
  0        0
  1        1
  10       2
  11       3
100        4
 101       5
 110       6
 111       7
1000       8
1111       F
0001 0000   10
0001 0001  11
0001 1111  1F
0010 0000  20
0b1010 1010
  A     A
  0xAA
  (10 * 16) + 10 = 170
  0b1100 0011
     C     3
     0xC3
     (12 * 16) + 3 --> 160 + 32 + 3 = 195
 R   G  B
#ff ff ff
#00 00 00
