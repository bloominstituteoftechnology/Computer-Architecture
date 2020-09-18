import sys
​
"""
Get the file path from the command line
Sanitize the data from that file
	Ignore blank lines, whitespace, comments
	Splitting the input file per line
	Turn into program instructions (str->int)
"""
# These all mean the same thing:
#   Index into the memory array
#   Address
#   Location
#   Pointer
​
memory = [0] * 256
​
if len(sys.argv) != 2:
	print("usage: comp.py filename")
	sys.exit(1)
​
try:
	address = 0
​
	with open(sys.argv[1]) as f:
		for line in f:
			t = line.split('#')
			n = t[0].strip()
​
			if n == '':
				continue
​
			try:
				n = int(n)
			except ValueError:
				print(f"Invalid number '{n}'")
				sys.exit(1)
​
			memory[address] = n
			address += 1
​
except FileNotFoundError:
	print(f"File not found: {sys.argv[1]}")
	sys.exit(2)
​
registers = [0] * 8  # R0-R7
​
# "Variables" in hardware. Known as "registers".
# There are a fixed number of registers
# They have fixed names
#  R0, R1, R2, ... , R6, R7
​
pc = 0  # Program Counter, address of the currently-executing instuction
​
running = True
​
while running:
	ir = memory[pc]  # Instruction Register, copy of the currently-executing instruction
​
	if ir == 1:  # PRINT_BEEJ
		print("Beej!")
		pc += 1
​
	elif ir == 2:
		running = False
​
	elif ir == 3:  # SAVE_REG (LDI on the LS8)
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		registers[reg_num] = value
		pc += 3
​
	elif ir == 4:  # PRINT_REG
		reg_num = memory[pc + 1]
		print(registers[reg_num])
		pc += 2
​
	else:
		print(f"Unknown instruction {b}")
​
	"""
	# For the LS-8 to move the PC
​
	number_of_operands = (ir & 0b11000000) >> 6
​
	how_far_to_move_pc = number_of_operands + 1
​
	pc += how_far_to_move_pc
	"""
    ####################################################################

    # Hello! This is my program!
                      
1  # PRINT_BEEJ
       1  # PRINT_BEEJ
1  # PRINT_BEEJ
1  # PRINT_BEEJ
​
3  # SAVE_REG R1,99
1
99
​
4  # PRINT_REG R1
1
2  # HALT

###########################################################



1  # PRINT_BEEJ  Address 0
3  # SAVE_REG R1,37
1
37
4  # PRINT_REG R1
1
2  # HALT

###########################################

Bitwise Operations
------------------
Math ops that work 1 bit at a time in a number.
A  B   A & B   (& is bitwise AND)
--------------
0  0     0
0  1     0
1  0     0
1  1     1
A  B   A | B   (| is bitwise OR)
--------------
0  0     0
0  1     1
1  0     1
1  1     1
A  B   A ^ B   (^ is bitwise XOR, "exclusive OR")
--------------
0  0     0
0  1     1
1  0     1
1  1     0
A   ~A   (~ is bitwise NOT)
------
0    1
1    0
  0b01010101
& 0b11100011
------------
  0b01000001 == 64
In general:
OR can be used to set bits to 1
AND can be used to clear bits to 0
      vv
  0b111001
& 0b110011  "AND mask"--stencil
----------
  0b110001
      ^^
      vv
  0b111001
| 0b001100  Use OR to force these two bits to 1 in the output
----------
  0b111101
      ^^
Bit shifting
------------
  111001  >> shift right
  011100  << shift left
  001110
  000111
  000011
  000001
  000000
123456 >>
012345
001234
000123
000012
000001
000000
      123456 <<
     1234560 <<
    12345600 <<
   123456000 <<
 vv
12345 -> [do some stuff] -> 23
.MM..
02300
00230
00023
   ^^
To extract individual numbers from inside a value, mask and shift.
