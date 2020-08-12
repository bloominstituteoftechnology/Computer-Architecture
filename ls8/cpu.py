"""CPU functionality."""

import sys

TGREEN =  '\033[32m'
TRED = '\033[31m'
TYELLOW = '\033[33m'
ENDC = '\033[m'

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.HLT = '1'
        self.LDI = '10000010'
        self.PRN = '1000111'
        self.MULT = '10100010'
        self.running = True        
        
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if len(sys.argv) < 2:
            print(TRED + 'File to open is: "examples/mult.ls8"', ENDC)
            sys.exit()
        try: 
            with open(sys.argv[1]) as file:
                for instruction in file:
                    inst = instruction.split("#")[0]
                    if inst == '':
                        continue
                    if inst[0] == '1' or inst [0] == '0':
                        num = inst[:8]
                        self.ram[address] = int(inst, 2)
                        address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found.')    
  
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        if op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, addr):
        return self.ram[addr]
    
    def ram_write(self, val, addr):
        self.ram[addr] = val
    
    def run(self):
        """Run the CPU."""
        pc = self.pc
        HLT = self.HLT
        LDI = self.LDI
        PRN = self.PRN
        MULT = self.MULT
        running = self.running
        
        while running:
            command = bin(self.ram_read(pc))[2:] 
            operand_a = self.ram_read(pc + 1)
            operand_b = self.ram_read(pc + 2)
            
            add_to_counter = (int(command, 2) >> 6) + 1
              
            if command == LDI:
                self.reg[operand_a] = operand_b
            elif command == MULT:
                self.alu("MULT", operand_a, operand_b)
            elif command == PRN:
                print(TGREEN + str(self.reg[operand_a]) + ENDC, end=', => ' )
            elif command == HLT:
                print(TYELLOW + "Program halted." + ENDC)
                running = False
              
            pc += add_to_counter