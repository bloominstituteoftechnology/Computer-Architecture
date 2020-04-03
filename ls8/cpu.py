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
        # FL: Flags
        self.E = 0
        self.L = 0
        self.G = 0
        # Interrupt Addresses
        self.I = [0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF]
        # RAM
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
        self.reg = [0] * 8

        self.IM = 5
        self.IS = 6
        self.SP = 7

        self.reg[self.IM] = False # interrupt mask (IM)
        self.reg[self.IS] = False # interrupt status (IS)
        self.reg[self.SP] = 0xF3 # stack pointer (SP)

        """
        Branchtable
        """
        self.branchtable = {}
        # OTHERS
        self.branchtable[0b00000001] = self.HLT
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b10000110] = self.ADDI
        self.branchtable[0b01000111] = self.PRN
        """
        NOP
        """
        self.branchtable[0b00000000] = self.NOP
        """
        ALU Operations
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
        self.branchtable[0b10100000] = self.ALU_ADD
        self.branchtable[0b10100001] = self.ALU_SUB
        self.branchtable[0b10100010] = self.ALU_MUL
        self.branchtable[0b10100011] = self.ALU_DIV
        self.branchtable[0b10100100] = self.ALU_MOD
        self.branchtable[0b01100101] = self.ALU_INC
        self.branchtable[0b01100110] = self.ALU_DEC
        self.branchtable[0b10100111] = self.ALU_CMP
        self.branchtable[0b10101000] = self.ALU_AND
        self.branchtable[0b01101001] = self.ALU_NOT
        self.branchtable[0b10101010] = self.ALU_OR
        self.branchtable[0b10101011] = self.ALU_XOR
        self.branchtable[0b10101100] = self.ALU_SHL
        self.branchtable[0b10101101] = self.ALU_SHR
        """
        Stack
        """
        self.branchtable[0b01000101] = self.PUSH
        self.branchtable[0b01000110] = self.POP
        """
        CALL & RET
        """
        self.branchtable[0b01010000] = self.CALL
        self.branchtable[0b00010001] = self.RET
        """
        JUMPS
        """
        self.branchtable[0b01010100] = self.JMP
        self.branchtable[0b01010101] = self.JEQ
        self.branchtable[0b01010110] = self.JNE
        """
        Interrupts
        """
        self.branchtable[0b10000100] = self.ST
        self.branchtable[0b01010010] = self.INT
        self.branchtable[0b00010011] = self.IRET

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename, 'r') as file:
                allLines = file.readlines()
                for i in range(0, len(allLines)):
                    line = allLines[i].replace('\n','').strip()
                    if '#' in allLines[i]:
                        line = allLines[i].split('#')[0].strip()
                    if len(line) > 0:
                        self.ram[address] = int(line, 2)
                        address += 1
            self.canRun = True
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def regLimit(self, address):
        self.reg[address] = self.reg[address] & 0xFF

    def ALU_ADD(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]
        self.regLimit(reg_a)
        
    def ALU_SUB(self, reg_a, reg_b):
        self.reg[reg_a] -= self.reg[reg_b]
        self.regLimit(reg_a)

    def ALU_MUL(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]
        self.regLimit(reg_a)
        
    def ALU_DIV(self, reg_a, reg_b):
        if self.reg[reg_b] is not 0:
            self.reg[reg_a] /= self.reg[reg_b]
            self.regLimit(reg_a)
        else:
            print('You cannot divide by zero!')
            self.HLT()
        
    def ALU_MOD(self, reg_a, reg_b):
        if self.reg[reg_b] is not 0:
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
            self.regLimit(reg_a)
        else:
            print('You cannot divide by zero!')
            self.HLT()
        
    def ALU_INC(self, reg_a):
        self.reg[reg_a] += 1
        self.regLimit(reg_a)
        
    def ALU_DEC(self, reg_a):
        self.reg[reg_a] -= 1
        self.regLimit(reg_a)
        
    def ALU_CMP(self, reg_a, reg_b):
        """
        Compare the values in two registers.
        * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
        * If registerA is less than registerB, set the Less-than `L` flag to 1,
        otherwise set it to 0.
        * If registerA is greater than registerB, set the Greater-than `G` flag
        to 1, otherwise set it to 0.
        """
        valA = self.reg[reg_a]
        valB = self.reg[reg_b]
        self.E = int(valA == valB)
        self.L = int(valA < valB)
        self.G = int(valA > valB)
        
    def ALU_AND(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        self.regLimit(reg_a)
        
    def ALU_NOT(self, reg_a):
        self.reg[reg_a] = ~self.reg[reg_a]
        
    def ALU_OR(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        
    def ALU_XOR(self, reg_a, reg_b):
        """
        Perform a bitwise-XOR between the values in registerA and registerB, storing the
        result in registerA.
        """
        self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        
    def ALU_SHL(self, reg_a, reg_b):
        """
        Shift the value in registerA left by the number of bits specified in registerB,
        filling the low bits with 0.
        """
        self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        
    def ALU_SHR(self, reg_a, reg_b):
        """
        Shift the value in registerA right by the number of bits specified in registerB,
        filling the high bits with 0.
        """
        self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

    def getOperation(self, identifier):
        if identifier in self.branchtable:
            return self.branchtable[identifier]
        raise Exception("Unsupported operation")
    
    def HLT(self):
        """HLT operation"""
        self.canRun = False
        return False

    def NOP(self):
        """
        No operation. Do nothing for this instruction.
        """
        return True

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
        while self.canRun:
            # get instruction
            instruction = self.ram_read(self.pc)
            # save it in instruction register
            self.ir[self.pc] = instruction
            # get operation name
            # print(f'run -> {instruction:08b}')
            operation = self.getOperation(instruction)
            # print(f'run {instruction:08b} -> pc {self.pc}')
            # decode instruction
            instruct = "{0:8b}".format(instruction)
            # operands = int(instruct[:2].strip() or '00', 2)
            operands = instruction >> 6
            # get param 1
            instruct_a = self.ram_read(self.pc + 1)
            # get param 2
            instruct_b = self.ram_read(self.pc + 2)

            if operands == 1:
                operation(instruct_a)
            elif operands == 2:
                operation(instruct_a, instruct_b)
            else:
                operation()
            
            self.pc += int(operands) + 1

    def ram_read(self, mar):
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
        if mar in self.ram:
            return self.ram[mar]
        return None

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        return self.ram[mar]

    def LDI(self, register, value):
        """
        LDI register immediate
        Set the value of a register to an integer.
        Machine code:
            10000010 00000rrr iiiiiiii
            82 0r ii
        """
        # print(f'LDI -> {register:08b} = {value:08b}')
        self.reg[int(register)] = int(value)
        return self.reg[int(register)]

    def ADDI(self, register, value):
        """
        ADDI
        Add an immediate value to a register
        """
        self.reg[int(register)] += value
        return self.reg[int(register)]

    def PRN(self, register):
        """
        PRN register pseudo-instruction
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        Machine code:
            01000111 00000rrr
            47 0r
        """
        numericValue = int(self.reg[int(register)])
        print(numericValue)
        return numericValue
    
    def PUSH(self, address):
        """
        Push the value in the given register on the stack.
        1. Decrement the `SP`.
        2. Copy the value in the given register to the address pointed to by
        `SP`.
        Machine code:
        ```
        01000101 00000rrr
        45 0r
        ```
        """
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[address]

    def POP(self, address):
        """
        Pop the value at the top of the stack into the given register.
        1. Copy the value from the address pointed to by `SP` to the given register.
        2. Increment `SP`.
        Machine code:
        ```
        01000110 00000rrr
        46 0r
        ```
        """
        if self.reg[self.SP] < 0xF3:
            self.reg[address] = self.ram[self.reg[self.SP]]
            self.reg[self.SP] += 1
            return self.reg[address]
        else:
            raise Exception("Cannot pop from empty stack!")

    def CALL(self, address):
        """
        Calls a subroutine (function) at the address stored in the register.
        1. The address of the ***instruction*** _directly after_ `CALL` is
        pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        2. The PC is set to the address stored in the given register. 
        We jump to that location in RAM and execute the first instruction in the subroutine. 
        The PC can move forward or backwards from its current location.
        Machine code:
        ```
        01010000 00000rrr
        50 0r
        ```
        """
        # print(f'CALL -> go to reg {address:08b}, {self.reg[address]}')
        # PUSH
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.pc + 1
        # SET PC
        self.pc = self.reg[address] - 2 # -2 cause operands

    def RET(self):
        """
        Return from subroutine.
        Pop the value from the top of the stack and store it in the `PC`.
        Machine Code:
        ```
        00010001
        11
        ```
        """
        # POP & SET PC
        self.pc = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

    def JMP(self, address):
        """
        Jump to the address stored in the given register.
        Set the `PC` to the address stored in the given register.
        Machine code:
        ```
        01010100 00000rrr
        54 0r
        ```
        """
        self.pc = self.reg[address] - 2 # -2 cause operands
    
    def JEQ(self, address):
        """
        If `equal` flag is set (true), jump to the address stored in the given register.
        Machine code:
        ```
        01010101 00000rrr
        55 0r
        ```
        """
        if self.E is True or self.E is 1:
            self.JMP(address)

    def JNE(self, address):
        """
        If `E` flag is clear (false, 0), jump to the address stored in the given
        register.
        Machine code:
        ```
        01010110 00000rrr
        56 0r
        ```
        """
        if self.E is False or self.E is 0:
            self.JMP(address)

    def ST(self, reg_a, reg_b):
        """
        Store value in registerB in the address stored in registerA.
        This opcode writes to memory.
        Machine code:
        ```
        10000100 00000aaa 00000bbb
        84 0a 0b
        ```
        """
        self.ram_write(self.reg[reg_a], self.reg[reg_b])

    def INT(self, address):
        """
        Issue the interrupt number stored in the given register.
        This will set the _n_th bit in the `IS` register to the value in the given
        register.
        Machine code:
        ```
        01010010 00000rrr
        52 0r
        ```
        """
        interruptNum = self.reg[address]
        #self.reg[self.IS] = ""
        #pass

    def IRET(self):
        """
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
        """
        pass