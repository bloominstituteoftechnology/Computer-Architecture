import sys

class CPU:
    # Main

    HLT = 0b00000001
    LDI = 0b10000010
    PRN = 0b01000111
    ADD = 0b10100000
    MUL = 0b10100010
    PUSH = 0b01000101
    POP = 0b01000110
    CALL = 0b01010000
    RET = 0b00010001
    CMP = 0b10100111
    JMP = 0b01010100
    JEQ = 0b01010101
    JNE = 0b01010110

    def __init__(self):
        # Constructing the CPU
        self.programCounter = 0
        self.ram = [0] * 256
        self.register = [0] * 8
        self.stackPointer = 7
        self.register[self.stackPointer] = 0xF4
        self.running = True
        self.flagsRegister = 0b00000000

    # finds the location in ram based on 'address'
    def read(self, address):
        return self.ram[address]

    
    def write(self, address, value):
        self.ram[address] = value

    def load(self):
        address = 0

        if len(sys.argv) != 2:
            print("Wrong number of arguments")
            sys.exit(1)
        with open(sys.argv[1]) as f:
            for line in f:
                line_split = line.split("#")
                command = line_split[0].strip()
                if command == '':
                    continue
                else:
                    self.ram[address] = int(command[:8], 2)
                    address += 1
    
    def alu(self, operation, register_a, register_b):
        if operation == self.ADD:
            self.register[register_a] += self.register[register_b]
            self.programCounter += 3
        elif operation == self.HLT:
            self.running = False
            self.programCounter += 1
        elif operation == self.LDI:
            self.register[register_a] = register_b
            self.programCounter += 3
        elif operation == self.PRN:
            print(self.register[register_a])
            self.programCounter += 2
        elif operation == self.MUL:
            self.register[register_a] *= self.register[register_b]
            self.programCounter += 3
        elif operation == self.PUSH:
            registerAddress = self.ram[self.programCounter + 1]
            value = self.register[registerAddress]
            self.register[self.stackPointer] -= 1
            self.ram[self.register[self.stackPointer]] = value
            self.programCounter += 2
        elif operation == self.POP:
            registerAddress = self.ram[self.programCounter + 1]
            self.register[registerAddress] = self.ram[self.register[self.stackPointer]]
            self.register[self.stackPointer] += 1
            self.programCounter += 2
        elif operation == self.CALL:
            self.register[self.stackPointer] -= 1
            self.ram[self.register[self.stackPointer]] = self.programCounter + 2
            registerNumber = self.ram[self.programCounter + 1]
            self.programCounter = self.register[registerNumber]
        elif operation == self.CMP:
            if self.register[register_a] < self.register[register_b]:
                self.flagsRegister = 0b00000100
            elif self.register[register_a] == self.register[register_b]:
                self.flagsRegister = 0b00000001
            self.programCounter += 3
        elif operation == self.JMP:
            register = self.read(self.programCounter + 1)
            self.programCounter = self.register[register]
        elif operation == self.JNE:
            register = self.read(self.programCounter + 1)
            if self.flagsRegister & 0b00000001 == False:
                self.programCounter = self.register[register]
            else:
                self.programCounter += 2
        elif operation == self.JEQ:
            register = self.read(self.programCounter + 1)
            if self.flagsRegister & 0b00000001:
                self.programCounter = self.register[register]
            else:
                self.programCounter += 2
        else:
            raise Exception("Unsupported operation")       

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.programCounter,
            self.read(self.programCounter),
            self.read(self.programCounter + 1),
            self.read(self.programCounter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        while self.running:
            IR = self.ram[self.programCounter]
            register_a = self.ram[self.programCounter + 1]
            register_b = self.ram[self.programCounter + 2]

            self.alu(IR, register_a, register_b)