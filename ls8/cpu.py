"""CPU functionality."""

import sys
from datetime import datetime
from  msvcrt import kbhit, getch

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Initialize Register
        self.reg = [0] * 8
        self.reg[7] = 0xF4

        # Initialize Memory
        self.ram = [0] * 256

        # Initialize internal registers
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0

        # Initialize operation values
        self.operand_a = 0
        self.operand_b = 0

        # Initialize halt as false. CPU does not start halted

        self.halt = False

        # Initialize pc_override for when pc is manually set by function

        self.pc_override = False

        # Intitialize interrupt 

        self.interrupt = True

        # Initialize branch_table
        self.branch_table = {}
        self.branch_table[0b10000010] = self.LDI
        self.branch_table[0b01000111] = self.PRN
        self.branch_table[0b00000001] = self.HLT
        self.branch_table[0b01000101] = self.PUSH
        self.branch_table[0b01000110] = self.POP
        self.branch_table[0b01010000] = self.CALL
        self.branch_table[0b00010001] = self.RET
        self.branch_table[0b01010010] = self.INT
        self.branch_table[0b00010011] = self.IRET
        self.branch_table[0b01010101] = self.JEQ
        self.branch_table[0b01011010] = self.JGE
        self.branch_table[0b01010111] = self.JGT
        self.branch_table[0b01011001] = self.JLE
        self.branch_table[0b01011000] = self.JLT
        self.branch_table[0b01010100] = self.JMP
        self.branch_table[0b01010110] = self.JNE
        self.branch_table[0b10000011] = self.LD
        self.branch_table[0b00000000] = self.NOP
        self.branch_table[0b01001000] = self.PRA
        self.branch_table[0b10000100] = self.ST


        
        
        # Initialize alu_table
        self.alu_table = {}
        self.alu_table[0b10100010] = "MUL"
        self.alu_table[0b10100000] = "ADD"
        self.alu_table[0b10101000] = "AND"
        self.alu_table[0b10100111] = "CMP"
        self.alu_table[0b01100110] = "DEC"
        self.alu_table[0b10100011] = "DIV"
        self.alu_table[0b01100101] = "INC"
        self.alu_table[0b10100100] = "MOD"
        self.alu_table[0b01101001] = "NOT"
        self.alu_table[0b10101010] = "OR"
        self.alu_table[0b10101100] = "SHL"
        self.alu_table[0b10101101] = "SHR"
        self.alu_table[0b10100001] = "SUB"
        self.alu_table[0b10101011] = "XOR"

        # Initialize Interupt Table
        self.interrupt_table = {}
        self.interrupt_table[0b00000001] = 0xF8
        self.interrupt_table[0b00000010] = 0xF9


    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram_write(address, instruction)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000100
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "DIV":
            if self.reg[reg_b] == 0:
                print("Error: Cannot divide by zero!")
                self.halt = True
            else:
                self.reg[reg_a] /= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                print("Error: Cannot divide by zero!")
                self.halt = True
            else:
                self.reg[reg_a] %= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a] 
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]    
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

    def ram_read(self, address):
        """
        Function that reads from memory. Takes in the address to read.
        Returns the value stored at that address in the RAM.
        """
        self.mar = address
        self.mdr = self.ram[self.mar]

        return self.mdr

    def ram_write(self, address, value):
        """
        Function that writes to memory. Takes in the value to write,
        the address to write to. Saves value at the given address.
        """
        self.mar = address
        self.ram[self.mar] = value
        self.mdr = self.ram[self.mar]

    def run(self):
        """Run the CPU."""
        time_delta = 0
        start_time = datetime.now()
        while not self.halt: 
            #self.trace()  
            # print(datetime.now())   
            self.ir = self.ram_read(self.pc)
            self.operand_a = self.ram_read(self.pc + 1)
            self.operand_b = self.ram_read(self.pc + 2) 

            # reset pc_override to check if PC needs to be adjusted 
            self.pc_override = False

            # Determine if alu operation or branch_table operation
            bit_5 = (self.ir & 2 ** 5) >> 5

            if self.interrupt:
                current_time = datetime.now()
                time_delta = current_time - start_time
                if time_delta.total_seconds() >= 1:
                    start_time = datetime.now()
                    self.reg[6] |= 0b00000001
                if kbhit():
                    self.ram_write(0xF4, ord(getch().decode('ascii')))
                    self.reg[6] |= 0b00000010
                masked_interrupts = self.reg[5] & self.reg[6]
                for i in range(8): 
                    interrupt_happened = ((masked_interrupts >> i) & 1) == 1
                    if interrupt_happened:
                        self.ir = 0b01010010
                        
                        
            if bit_5:
                op = self.alu_table[self.ir]
                self.alu(op, self.operand_a, self.operand_b)
            
            if not bit_5:
                self.branch_table[self.ir]()

            if not self.pc_override:
                bit_6 = (self.ir & 2 ** 6) >> 6
                bit_7 = (self.ir & 2 ** 7) >> 7

                if bit_6: 
                    self.pc += 2
                if bit_7:
                    self.pc += 3
        sys.exit()
                

    def LDI(self):
        """
        Set register to this value
        """
        self.reg[self.operand_a] = self.operand_b

    def PRN(self):
        """
        Prints numeric value stored at register address
        """
        print(self.reg[self.operand_a])

    def HLT(self):
        """
        Sets halt value to true
        """
        self.halt = True

    def PUSH(self, value=None):
        """
        Pushes value at given register on to computer stack
        """
        self.reg[7] -= 1
        if value is None:
            value = self.reg[self.operand_a]
        self.ram_write(self.reg[7], value)
    
    def POP(self, register=True):
        """
        Pops value at current stack pointer off the stack 
        and stores it at the given register
        """
        value = self.ram_read(self.reg[7])
        if register:
            self.reg[self.operand_a] = value
        else:
            return value
        self.reg[7] += 1

    def CALL(self):
        """
        Calls a subroutine (function) stored at the address in the register.
        
        The address of the instruction directly after CALL is pushed onto the stack. 
        The PC is set to the address stored in the given register.
        """
        self.pc_override = True
        self.PUSH(self.pc + 2)
        self.pc = self.reg[self.operand_a]

    def RET(self):
        """
        Returns from subroutine.
        Pop the value from the top of the stack and store it in the PC.
        """
        self.pc = self.POP(register=False)

    def INT(self):
        """
        Issue the interrupt number stored in the given register.

        This will set the _n_th bit in the IS register to the value in the given register.
        """
        self.pc_override = True
        # Disable further interrupts.
        self.interrupt = False
        # Clear the bit in the IS register.
        im_reg = self.reg[5]
        self.reg[6] = 0
        # The PC register is pushed on the stack.
        self.PUSH(self.pc)
        # The FL register is pushed on the stack.
        self.PUSH(self.fl)
        # Registers R0-R6 are pushed on the stack in that order.
        for i in range(7):
            self.PUSH(self.reg[i])
        # Set the PC is set to the handler address. 
        self.pc = self.ram_read(self.interrupt_table[im_reg])


    def IRET(self):
        """
        Return from an interrupt handler.

        The following steps are executed:

            Registers R6-R0 are popped off the stack in that order.
            The FL register is popped off the stack.
            The return address is popped off the stack and stored in PC.
            Interrupts are re-enabled
        """
        self.pc_override = True
        # Registers R6-R0 are popped off the stack in that order.
        for i in range(7):
            self.reg[6 - i] = self.POP(register=False)
        # The FL register is popped off the stack.
        self.fl = self.POP(register=False)
        # The return address is popped off the stack and stored in PC.
        self.pc = self.POP(register=False)
        # Interrupts are re-enabled
        self.interrupt = True


    def JEQ(self):
        """
        If equal flag is set (true), jump to the address stored in the given register.
        """
        bit_0 = (self.fl & 2 ** 0) >> 0
        if bit_0:
            self.pc_override = True
            self.pc = self.reg[self.operand_a]
        
    def JGE(self):
        """
        If greater-than flag or equal flag is set (true), 
        jump to the address stored in the given register.
        """
        bit_0 = (self.fl & 2 ** 0) >> 0
        bit_1 = (self.fl & 2 ** 1) >> 1

        if bit_0 or bit_1:
           self.pc_override = True
           self.pc = self.reg[self.operand_a]

    def JGT(self):
        """
        If greater-than flag is set (true), jump to the address stored in the given register.
        """ 
        bit_1 = (self.fl & 2 ** 1) >> 1

        if bit_1:
           self.pc_override = True
           self.pc = self.reg[self.operand_a]

    def JLE(self):
        """
        If less-than flag or equal flag is set (true), jump to the address stored in the given register.
        """
        bit_0 = (self.fl & 2 ** 0) >> 0
        bit_2 = (self.fl & 2 ** 2) >> 2

        if bit_0 or bit_2:
           self.pc_override = True
           self.pc = self.reg[self.operand_a]
    
    def JLT(self):
        """
        If less-than flag is set (true), jump to the address stored in the given register.
        """
        bit_2 = (self.fl & 2 ** 2) >> 2

        if bit_2:
           self.pc_override = True
           self.pc = self.reg[self.operand_a]

    def JMP(self):
        """
        Jump to the address stored in the given register.
        """
        self.pc_override = True
        self.pc = self.reg[self.operand_a]

    def JNE(self):
        """
        If E flag is clear (false, 0), jump to the address stored in the given register.
        """
        bit_0 = (self.fl & 2 ** 0) >> 0
        
        if not bit_0:
            self.pc_override = True
            self.pc = self.reg[self.operand_a]


    def LD(self):
        """
        Loads registerA with the value at the memory address stored in registerB.

        This opcode reads from memory.
        """
        self.reg[self.operand_a] = self.ram_read(self.reg[self.operand_b])

    def NOP(self):
        """
        No operation. Do nothing for this instruction.
        """
        pass

    def PRA(self):
        """
        Print alpha character value stored in the given register.
        """
        print(chr(self.reg[self.operand_a]))

    def ST(self):
        """
        Store value in registerB in the address stored in registerA.
        This opcode writes to memory.
        """
        self.ram_write(
            self.reg[self.operand_a],
            self.reg[self.operand_b]
            )




