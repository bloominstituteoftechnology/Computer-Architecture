
def ldi(cpu, register, value):
	cpu.registers[register] = value


def hlt(cpu, _1, _2):
	cpu.fl = cpu.fl & 0b01111111


def prn(cpu, register, _2):
	print(cpu.registers[register])


ops = {
	0b0010: ldi,
	0b0001: hlt,
	0b0111: prn,
}
