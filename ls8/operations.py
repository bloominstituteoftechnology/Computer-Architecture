
def nop(cpu, _1, _2):
	pass


def ldi(cpu, register, value):
	cpu.registers[register] = value


def hlt(cpu, _1, _2):
	cpu.fl = cpu.fl & 0b01111111


def prn(cpu, register, _2):
	print(cpu.registers[register])


def mul(cpu, register_A, register_B):
	cpu.alu('MUL', register_A, register_B)


ops = {
	0b00000000: nop,
	0b10000010: ldi,
	0b00000001: hlt,
	0b01000111: prn,
	0b10100010: mul,
}
