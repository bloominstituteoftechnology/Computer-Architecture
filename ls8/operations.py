


def ADD(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`ADD registerA registerB`

	Add the value in two registers and store the result in registerA.

	Machine code:
	```
	10100000 00000aaa 00000bbb
	A0 0a 0b
	```
	'''

	cpu.alu('ADD', register_A, register_B)


def AND(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`AND registerA registerB`

	Bitwise-AND the values in registerA and registerB, then store the result in
	registerA.

	Machine code:
	```
	10101000 00000aaa 00000bbb
	A8 0a 0b
	```
	'''

	cpu.alu('AND', register_A, register_B)


def CALL(cpu, register, *_):
	'''
	`CALL register`

	Calls a subroutine (function) at the address stored in the register.

	1. The address of the ***instruction*** _directly after_ `CALL` is
	pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
	2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.

	Machine code:
	```
	01010000 00000rrr
	50 0r
	```
	'''

	cpu.SP -= 1
	cpu.ram_write(cpu.SP, cpu.pc + 2)

	cpu.pc = cpu.registers[register]


def CMP(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`CMP registerA registerB`

	Compare the values in two registers.

	* If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.

	* If registerA is less than registerB, set the Less-than `L` flag to 1,
	otherwise set it to 0.

	* If registerA is greater than registerB, set the Greater-than `G` flag
	to 1, otherwise set it to 0.

	Machine code:
	```
	10100111 00000aaa 00000bbb
	A7 0a 0b
	```
	'''

	cpu.alu('CMP', register_A, register_B)


def DEC(cpu, register, *_):
	'''
	*This is an instruction handled by the ALU.*

	`DEC register`

	Decrement (subtract 1 from) the value in the given register.

	Machine code:
	```
	01100110 00000rrr
	66 0r
	```
	'''

	cpu.alu('DEC', register, 0b00000000)


def DIV(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`DIV registerA registerB`

	Divide the value in the first register by the value in the second,
	storing the result in registerA.

	If the value in the second register is 0, the system should print an
	error message and halt.

	Machine code:
	```
	10100011 00000aaa 00000bbb
	A3 0a 0b
	```
	'''

	cpu.alu('DIV', register_A, register_B)


def HLT(cpu, *_):
	'''
	`HLT`

	Halt the CPU (and exit the emulator).

	Machine code:
	```
	00000001
	01
	```
	'''

	cpu.fl = cpu.fl & 0b01111111


def INC(cpu, register, *_):
	'''
	*This is an instruction handled by the ALU.*

	`INC register`

	Increment (add 1 to) the value in the given register.

	Machine code:
	```
	01100101 00000rrr
	65 0r
	```
	'''

	cpu.alu('INC', register, 0b00000000)


def INT(cpu, register, *_):
	'''
	`INT register`

	Issue the interrupt number stored in the given register.

	This will set the _n_th bit in the `IS` register to the value in the given
	register.

	Machine code:
	```
	01010010 00000rrr
	52 0r
	```
	'''

	cpu.IS = cpu.IS | (1 << register)


def IRET(cpu, *_):
	'''
	`IRET`

	Return from an interrupt handler.

	The following steps are executed:

	1. Registers R6-R0 are popped off the stack in that order.
	2. The `FL` register is popped off the stack.
	3. The return address is popped off the stack and stored in `PC`.
	4. Interrupts are re-enabled

	Machine code:
	```
	00010011
	13
	```
	'''

	for r in range(6, -1, -1):
		POP(cpu, r)

	cpu.fl = cpu.ram_read(cpu.SP)
	cpu.SP += 1
	cpu.pc = cpu.ram_read(cpu.SP)
	cpu.SP += 1

	cpu.fl = cpu.fl | 0b01000000



def JEQ(cpu, register, *_):
	'''
	`JEQ register`

	If `equal` flag is set (true), jump to the address stored in the given register.

	Machine code:
	```
	01010101 00000rrr
	55 0r
	```
	'''

	# print(f'Flags: {cpu.fl:08b}')
	if cpu.fl & 0b00000001:
		cpu.pc = cpu.registers[register]
	else:
		cpu.pc += 2


def JGE(cpu, register, *_):
	'''
	`JGE register`

	If `greater-than` flag or `equal` flag is set (true), jump to the address stored
	in the given register.

	```
	01011010 00000rrr
	5A 0r
	```
	'''

	if cpu.fl & 0b00000011:
		cpu.pc = cpu.registers[register]
	else:
		cpu.pc += 2


def JGT(cpu, register, *_):
	'''
	`JGT register`

	If `greater-than` flag is set (true), jump to the address stored in the given
	register.

	Machine code:
	```
	01010111 00000rrr
	57 0r
	```
	'''

	if cpu.fl & 0b00000010:
		cpu.pc = cpu.registers[register]
	else:
		cpu.pc += 2


def JLE(cpu, register, *_):
	'''
	`JLE register`

	If `less-than` flag or `equal` flag is set (true), jump to the address stored in the given
	register.

	```
	01011001 00000rrr
	59 0r
	```
	'''

	if cpu.fl & 0b00000101:
		cpu.pc = cpu.registers[register]
	else:
		cpu.pc += 2


def JLT(cpu, register, *_):
	'''
	`JLT register`

	If `less-than` flag is set (true), jump to the address stored in the given
	register.

	Machine code:
	```
	01011000 00000rrr
	58 0r
	```
	'''

	if cpu.fl & 0b00000100:
		cpu.pc = cpu.registers[register]
	else:
		cpu.pc += 2


def JMP(cpu, register, *_):
	'''
	`JMP register`

	Jump to the address stored in the given register.

	Set the `PC` to the address stored in the given register.

	Machine code:
	```
	01010100 00000rrr
	54 0r
	```
	'''

	cpu.pc = cpu.registers[register]


def JNE(cpu, register, *_):
	'''
	`JNE register`

	If `E` flag is clear (false, 0), jump to the address stored in the given
	register.

	Machine code:
	```
	01010110 00000rrr
	56 0r
	```
	'''

	if not cpu.fl & 0b00000001:
		cpu.pc = cpu.registers[register]
	else:
		cpu.pc += 2


def LD(cpu, register_A, register_B, *_):
	'''
	`LD registerA registerB`

	Loads registerA with the value at the memory address stored in registerB.

	This opcode reads from memory.

	Machine code:
	```
	10000011 00000aaa 00000bbb
	83 0a 0b
	```
	'''

	cpu.registers[register_A] = cpu.ram_read(cpu.registers[register_B])


def LDI(cpu, register, value, *_):
	'''
	`LDI register immediate`

	Set the value of a register to an integer.

	Machine code:
	```
	10000010 00000rrr iiiiiiii
	82 0r ii
	```
	'''

	cpu.registers[register] = value


def MOD(cpu, register_A, register_B):
	'''
	*This is an instruction handled by the ALU.*

	`MOD registerA registerB`

	Divide the value in the first register by the value in the second,
	storing the _remainder_ of the result in registerA.

	If the value in the second register is 0, the system should print an
	error message and halt.

	Machine code:
	```
	10100100 00000aaa 00000bbb
	A4 0a 0b
	```
	'''

	cpu.alu('MOD', register_A, register_B)


def MUL(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`MUL registerA registerB`

	Multiply the values in two registers together and store the result in registerA.

	Machine code:
	```
	10100010 00000aaa 00000bbb
	A2 0a 0b
	```
	'''

	cpu.alu('MUL', register_A, register_B)


def NOP(cpu, *_):
	'''
	`NOP`

	No operation. Do nothing for this instruction.

	Machine code:
	```
	00000000
	00
	```
	'''

	pass


def NOT(cpu, register, *_):
	'''
	*This is an instruction handled by the ALU.*

	`NOT register`

	Perform a bitwise-NOT on the value in a register, storing the result in the register.

	Machine code:
	```
	01101001 00000rrr
	69 0r
	```
	'''

	cpu.alu('NOT', register, 0b00000000)


def OR(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`OR registerA registerB`

	Perform a bitwise-OR between the values in registerA and registerB, storing the
	result in registerA.

	Machine code:
	```
	10101010 00000aaa 00000bbb
	AA 0a 0b
	```
	'''

	cpu.alu('OR', register_A, register_B)


def POP(cpu, register, *_):
	'''
	`POP register`

	Pop the value at the top of the stack into the given register.

	1. Copy the value from the address pointed to by `SP` to the given register.
	2. Increment `SP`.

	Machine code:
	```
	01000110 00000rrr
	46 0r
	```
	'''

	cpu.registers[register] = cpu.ram_read(cpu.SP)
	cpu.SP += 1


def PRA(cpu, register, *_):
	'''
	`PRA register` pseudo-instruction

	Print alpha character value stored in the given register.

	Print to the console the ASCII character corresponding to the value in the
	register.

	Machine code:
	```
	01001000 00000rrr
	48 0r
	```
	'''

	# While chr technically returns Unicode, this does not cause problems
	# (As Unicode is a superset of ASCII)
	print(chr(cpu.registers[register]), end='')


def PRN(cpu, register, *_):
	'''
	`PRN register` pseudo-instruction

	Print numeric value stored in the given register.

	Print to the console the decimal integer value that is stored in the given
	register.

	Machine code:
	```
	01000111 00000rrr
	47 0r
	```
	'''

	print(cpu.registers[register])


def PUSH(cpu, register, *_):
	'''
	`PUSH register`

	Push the value in the given register on the stack.

	1. Decrement the `SP`.
	2. Copy the value in the given register to the address pointed to by
	`SP`.

	Machine code:
	```
	01000101 00000rrr
	45 0r
	```
	'''

	cpu.SP -= 1
	cpu.ram_write(cpu.SP, cpu.registers[register])


def RET(cpu, *_):
	'''
	`RET`

	Return from subroutine.

	Pop the value from the top of the stack and store it in the `PC`.

	Machine Code:
	```
	00010001
	11
	```
	'''

	cpu.pc = cpu.ram_read(cpu.SP)
	cpu.SP += 1


def SHL(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	Shift the value in registerA left by the number of bits specified in registerB,
	filling the low bits with 0.

	```
	10101100 00000aaa 00000bbb
	AC 0a 0b
	```
	'''

	cpu.alu('SHL', register_A, register_B)


def SHR(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	Shift the value in registerA right by the number of bits specified in registerB,
	filling the high bits with 0.

	```
	10101101 00000aaa 00000bbb
	AD 0a 0b
	```
	'''

	cpu.alu('SHR', register_A, register_B)


def ST(cpu, register_A, register_B, *_):
	'''
	`ST registerA registerB`

	Store value in registerB in the address stored in registerA.

	This opcode writes to memory.

	Machine code:
	```
	10000100 00000aaa 00000bbb
	84 0a 0b
	```
	'''

	cpu.ram_write(cpu.registers[register_A], cpu.registers[register_B])


def SUB(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`SUB registerA registerB`

	Subtract the value in the second register from the first, storing the
	result in registerA.

	Machine code:
	```
	10100001 00000aaa 00000bbb
	A1 0a 0b
	```
	'''

	cpu.alu('SUB', register_A, register_B)


def XOR(cpu, register_A, register_B, *_):
	'''
	*This is an instruction handled by the ALU.*

	`XOR registerA registerB`

	Perform a bitwise-XOR between the values in registerA and registerB, storing the
	result in registerA.

	Machine code:
	```
	10101011 00000aaa 00000bbb
	AB 0a 0b
	```
	'''

	cpu.alu('XOR', register_A, register_B)



ops = {
	0b10100000: ADD,
	0b10101000: AND,
	0b01010000: CALL,
	0b10100111: CMP,
	0b01100110: DEC,
	0b10100011: DIV,
	0b00000001: HLT,
	0b01100101: INC,
	0b01010010: INT,
	0b00010011: IRET,
	0b01010101: JEQ,
	0b01011010: JGE,
	0b01010111: JGT,
	0b01011001: JLE,
	0b01011000: JLT,
	0b01010100: JMP,
	0b01010110: JNE,
	0b10000011: LD,
	0b10000010: LDI,
	0b10100100: MOD,
	0b10100010: MUL,
	0b00000000: NOP,
	0b01101001: NOT,
	0b10101010: OR,
	0b01000110: POP,
	0b01001000: PRA,
	0b01000111: PRN,
	0b01000101: PUSH,
	0b00010001: RET,
	0b10101100: SHL,
	0b10101101: SHR,
	0b10000100: ST,
	0b10100001: SUB,
	0b10101011: XOR,
}

