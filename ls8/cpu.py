"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
     
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0

    
    def ram_read(self, MAR):
        # MAR = memory address register
        return self.ram[MAR]

    
    def ram_write(self, MAR, MDR):
        # MAR = memory address register
        # MDR = memory data register
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        if len(sys.argv) != 2:
            print("Usage: cpu.py filename")
            sys.exit(1)
        
        filename = sys.argv[1]

        try:
            with open(filename) as f:
                for line in f:
                    
                    instruction = line.split("#")[0].strip()
                    
                    if instruction == "":
                        continue

                    val = int(instruction, 2)    

                    self.ram_write(address, val)

                    address += 1

        except FileNotFoundError:
            print(f"File {filename} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        
        running = True

        while running:

            command = self.ram[self.pc]

            if command == 0b10000010: # LDI R0,8
                register_idx = self.ram[self.pc + 1]
                register_val = self.ram[self.pc + 2]
                self.registers[register_idx] = register_val
                self.pc += 3
            
            elif command == 0b01000111: # PRN R0
                register_idx = self.ram[self.pc + 1] 
                print(self.registers[register_idx])
                self.pc += 2

            elif command == 0b10100010: # MULT
                register_a_idx = self.ram[self.pc + 1]
                register_b_idx = self.ram[self.pc + 2]

                val = self.registers[register_a_idx] * self.registers[register_b_idx]

                self.registers[register_a_idx] = val

                self.pc += 3

            elif command == 0b00000001: # HLT
                self.pc += 1
                running = False
            
            else:
                print(f"Unknown instruction: {command}")
                sys.exit(1)


        
