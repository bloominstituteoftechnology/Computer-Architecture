"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.canRun = False
        """
        Internal Registers
        """
        # PC: Program Counter, address of the currently executing instruction
        self.pc = 0
        # IR: Instruction Register, contains a copy of the currently executing instruction
        self.ir = [0] * 256
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        self.mar = 0
        # MDR: Memory Data Register, holds the value to write or the value just read
        self.mdr = 0
        # FL: Flags
        self.fl = 0
        # ram
        self.ram = dict()
        """
        8 general-purpose 8-bit numeric registers R0-R7.
            R5 is reserved as the interrupt mask (IM)
            R6 is reserved as the interrupt status (IS)
            R7 is reserved as the stack pointer (SP)
        These registers only hold values between 0-255. 
        After performing math on registers in the emulator, bitwise-AND the result with 0xFF (255) 
        to keep the register values in that range.
        """
        self.reg = dict()

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        self.canRun = True


    def alu(self, op, reg_a, reg_b):
        """
        ALU operations.
        ADD  10100000 00000aaa 00000bbb
        SUB  10100001 00000aaa 00000bbb
        MUL  10100010 00000aaa 00000bbb
        DIV  10100011 00000aaa 00000bbb
        MOD  10100100 00000aaa 00000bbb
        INC  01100101 00000rrr
        DEC  01100110 00000rrr
        CMP  10100111 00000aaa 00000bbb
        AND  10101000 00000aaa 00000bbb
        NOT  01101001 00000rrr
        OR   10101010 00000aaa 00000bbb
        XOR  10101011 00000aaa 00000bbb
        SHL  10101100 00000aaa 00000bbb
        SHR  10101101 00000aaa 00000bbb
        """
        print(f'ALU [{op}] -> {reg_a}, {reg_b}')
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "MOD":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "INC":
            # self.reg[reg_a] ?? reg_b
            pass
        elif op == "DEC":
            # self.reg[reg_a] ?? reg_b
            pass
        elif op == "CMP":
            return self.reg[reg_a] == self.reg[reg_b]
        elif op == "AND":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "NOT":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "OR":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "XOR":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "SHL":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "SHR":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        else:
            raise Exception("Unsupported ALU operation")
    
    def getOperation(self, identifier):
        ALUIdentifier = int("{0:8b}".format(identifier)[4:], 2)
        if identifier == 0b00000001:
            return "HLT"
        elif identifier == 0b10000010:
            return "LDI"
        elif identifier == 0b01000111:
            return "PRN"
        elif ALUIdentifier == 0b0000:
            return "ADD"
        elif ALUIdentifier == 0b0001:
            return "SUB"
        elif ALUIdentifier == 0b0010:
            return "MUL"
        elif ALUIdentifier == 0b0011:
            return "DIV"
        elif ALUIdentifier == 0b0100:
            return "MOD"
        elif ALUIdentifier == 0b0101:
            return "INC"
        elif ALUIdentifier == 0b0110:
            return "DEC"
        elif ALUIdentifier == 0b0111:
            return "CMP"
        elif ALUIdentifier == 0b1000:
            return "AND"
        elif ALUIdentifier == 0b1001:
            return "NOT"
        elif ALUIdentifier == 0b1010:
            return "OR"
        elif ALUIdentifier == 0b1011:
            return "XOR"
        elif ALUIdentifier == 0b1100:
            return "SHL"
        elif ALUIdentifier == 0b1101:
            return "SHR"
        return None
    
    def hlt(self):
        """HLT operation"""
        self.canRun = False
        return False

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
        """
        Run the CPU.
        The instruction pointed to by the PC is fetched from RAM, decoded, and executed.
        If the instruction does not set the PC itself, the PC is advanced to point to the subsequent instruction.
        If the CPU is not halted by a HLT instruction, go to step 1.
        """
        pcAlterCommands = ['CALL','INT','IRET','JMP','JNE','JEQ','JGT','JGE','JLT','JLE','RET']
        while self.canRun:
            instruction = self.ram_read(self.pc)
            self.ir[self.pc] = instruction
            # get operation name
            operation = self.getOperation(instruction)

            if operation is 'HLT':
                self.hlt()

            # decode instruction
            instruct = "{0:8b}".format(instruction)
            operands = int(instruct[:2].strip() or '00', 2)
            alu = int(instruct[2].strip() or '0', 2)
            setPC = int(instruct[3].strip() or '0', 2)
            identifier = int(instruct[4:].strip() or '0000', 2)

            """ print(
                f'\n\nram_read {int(instruct,2):08b}', 
                f'\noperands {operands:02b}', 
                f'\nALU op? {alu:01b}', 
                f'\nsets PC? {setPC:01b}', 
                f'\ninstruct identifier {identifier:04b}'
            ) """
            # if it is an ALU operation
            if alu == 0b1:
                instruct_a = self.ram_read(self.pc + 1)
                instruct_b = self.ram_read(self.pc + 2)
                self.alu(operation, instruct_a, instruct_b)
            elif alu == 0b0: # else, if its not ALU operation
                # if it is LDI operation
                if operation == 'LDI':
                    # get the two arguments, registry and value
                    instruct_a = self.ram_read(self.pc + 1)
                    instruct_b = self.ram_read(self.pc + 2)
                    # run LDI
                    self.LDI(instruct_a, instruct_b)

                # if it is PRN operation
                elif operation == 'PRN':
                    # get the regitry argument
                    instruct_a = self.ram_read(self.pc + 1)
                    # run PRN
                    self.PRN(instruct_a)

            if setPC is not 0b1:
                # pc is advanced to subsequent instruction
                # print('self.pc +=', int(operands))
                self.pc += int(operands)
            else:
                self.pc += 1

            # self.trace()

    def ram_read(self, address):
        """
        Meanings of the bits in the first byte of each instruction: AABCDDDD
        AA Number of operands for this opcode, 0-2
        B 1 if this is an ALU operation
        C 1 if this instruction sets the PC
        DDDD Instruction identifier
        The number of operands AA is useful to know because 
        the total number of bytes in any instruction is the number of operands + 1 (for the opcode). 
        This allows you to know how far to advance the PC with each instruction.
        """
        if address in self.ram:
            return self.ram[address]
        return None

    def ram_write(self, address, value):
        self.ram[address] = value
        return self.ram[address]

    def LDI(self, register, value):
        """
        LDI register immediate
        Set the value of a register to an integer.
        Machine code:
            10000010 00000rrr iiiiiiii
            82 0r ii
        """
        self.ir[int(register)] = value
        self.pc += 1
        return self.ir[int(register)]

    def PRN(self, register):
        """
        PRN register pseudo-instruction
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        Machine code:
            01000111 00000rrr
            47 0r
        """
        print(int(self.ir[int(register)]))
        self.pc += 1
        return True