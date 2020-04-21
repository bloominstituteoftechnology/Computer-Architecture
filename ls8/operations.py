
def nop(cpu, *_):
	pass


def ldi(cpu, register, value, *_):
	cpu.registers[register] = value


def hlt(cpu, *_):
	cpu.fl = cpu.fl & 0b01111111


def prn(cpu, register, *_):
	print(cpu.registers[register])


def mul(cpu, register_A, register_B, *_):
	cpu.alu('MUL', register_A, register_B)


def push(cpu, register, *_):
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

	cpu.sc -= 1
	cpu.ram_write(cpu.sc, cpu.registers[register])


def pop(cpu, register, *_):
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

	cpu.registers[register] = cpu.ram_read(cpu.sc)
	cpu.sc += 1


def ret(cpu, *_):
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

	cpu.pc = cpu.ram_read(cpu.sc)
	cpu.sc += 1


def st(cpu, register_A, register_B):
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

	cpu.ram_write(cpu[register_A], cpu[register_B])

#
#
#
#
#


def ADD(cpu, register_A, register_B):
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


def AND(cpu, register_A, register_B):
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

	cpu.sc -= 1
	cpu.ram_write(cpu.sc, cpu.pc + 2)

	cpu.pc = cpu.registers[register]


def CMP(cpu, register_A, register_B):
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


def DIV(cpu, register_A, register_B):
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


ops = {
	0b10100000: ADD,
	0b10101000: AND,
	0b01010000: CALL,
	0b10100111: CMP,
	0b01100110: DEC,
	0b10100011: DIV,
	0b00000000: nop,
	0b10000010: ldi,
	0b00000001: hlt,
	0b01000111: prn,
	0b10100010: mul,
	0b01000110: pop,
	0b01000101: push,
	0b00010001: ret,
}
