"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    ops = {
        0x00: "NOP",   # no-op
        0x01: "HLT",   # halt; exit
        0x50: "CALL",  # call subroutine at register address
        0x11: "RET",   # return from subroutine
        0x52: "INT",   # interrupt
        0x13: "IRET",  # return from interrupt
        0x54: "JMP",   # jump to address in given reg
        0x55: "JEQ",   # if == flag true, jump to address in given reg
        0x56: "JNE",   # if E flag is clear, jump to address in given reg
        0x57: "JGT",   # if >, jump to address in given reg
        0x58: "JLT",   # if <
        0x59: "JLE",   # if < or ==
        0x5A: "JGE",   # if > or ==
        0x82: "LDI",   # set value of register to integer
        0x83: "LD",    # loads regA w/ value at mem address stored in regB
        0x84: "ST",    # store value in regB at address in regA
        0x48: "PRA",   # print alpha char value stored in given reg
        0x65: "INC",   # increment (ALU)
        0x66: "DEC",   # decrement (ALU)
        0xA7: "CMP",   # comparison (ALU)
        0xA8: "AND",   # bitwise-and (ALU)
        0x69: "NOT",   # bitwise-not (ALU)
        0xAA: "OR",    # bitwise-or (ALU)
        0xAB: "XOR",   # XOR (ALU)
        0xAC: "SHL",   # bitshift left (ALU)
        0xAD: "SHR",   # bitshift right (ALU)
    }
    def __init__(self):
        
        """Construct a new CPU."""
        
        self.ram = [0] * 256
        self.reg = [0] * 7
        self.reg.append(0xF4)
        self.pc = 0  # program counter (address of executing instruction)
        self.fl = 0  # flags
        self._dispatch = {
            0x01: self._hlt,
            0x82: self._ldi,  # load integer
            0x50: self._call,
            0x11: self._ret,
            0x47: self._prn,
            0x45: self._push,
            0x46: self._pop,
        }
        
        self._alu_dispatch = {
            0xA0: self._add,
            0xA1: self._sub,
            0xA2: self._mul,
            0xA3: self._div,
            0xA4: self._mod,
        }
        self.sp = 0xF3  # stack pointer
        self.running = False

    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, value, address):
        self.ram[address] = value
    def load(self):
        
        """Load a program into memory."""
        
        if len(sys.argv) < 2:
            print("ERROR: no filename argument")
            return
        address = 0
        with open(sys.argv[1], 'r') as program_file:
            for line in program_file:
                comment_index = line.find('#')
                if comment_index != -1:
                    line = line[:comment_index]
                line = line.strip()
                if len(line) == 0:
                    continue
                self.ram[address] = int(line, 2)
                address += 1
    def alu(self, ir, reg_a, reg_b):
        
        """ALU operations."""

        operation = self._alu_dispatch.get(ir)
        arg_count = self._arg_count(ir)

        if operation is None:
            raise Exception("Unsupported ALU operation")
        elif arg_count == 1:
            operation(reg_a)
        elif arg_count == 2:
            operation(reg_a, reg_b)
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    def _arg_count(self, ir):
        return ir >> 6
    def run(self):
        
        """Run the CPU."""
        self.running = True
        while self.running:
            ir = self.ram_read(self.pc)  # instruction register

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            args = self._arg_count(ir)

            if ir & 0b00100000:
                self.alu(ir, operand_a, operand_b)
        
                operation = self._dispatch.get(ir)

                if operation is None:
                    raise Exception("Unsupported ALU operation")
                    # return
                elif args == 1:
                    operation(operand_a)
                elif args == 2:
                    operation(operand_a, operand_b)
                else:
                    operation()  
        # self.run()
            if not ir & 0b00010000:
                self.pc += args + 1


    def _hlt(self):
        self.running = False
   
    def _ldi(self, reg_address, value):
        self.reg[reg_address] = value
        
    def _prn(self, reg_address):
        print(self.reg[reg_address])
        
    def _add(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
        
    def _sub(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] - self.reg[reg_b]
        
    def _mul(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        
    def _div(self, reg_a, reg_b):
        operand_b = self.reg[reg_b]
        if operand_b == 0:
            print("Error: Cannot divide by zero")
            self._hlt()
            return
        self.reg[reg_a] = self.reg[reg_a] / operand_b
        
    def _mod(self, reg_a, reg_b):
        operand_b = self.reg[reg_b]
        if operand_b == 0:
            print("Error: Cannot divide by zero")
            self._hlt()
            return
        self.reg[reg_a] = self.reg[reg_a] % operand_b
        
    def _inc(self, op):
        pass
    
    def _dec(self, op):
        pass
    
    def _cmp(self, op1, op2):
        pass
    
    def _and(self, op1, op2):
        pass
    
    def _not(self, op1, op2):
        pass
    def _or(self, op1, op2):
        pass
    
    def _xor(self, op1, op2):
        pass
    
    def _shl(self, op1, op2):
        pass
    
    def _shr(self, op1, op2):
        pass

    def _push(self, adr):
        self.sp -= 1
        self.ram[self.sp] = self.reg[adr]

    def _pop(self, adr):
        self.reg[adr] = self.ram[self.sp]
        self.sp += 1
    
    def _call(self, adr):
        reg0 = self.reg[0]  # temp value for register
        # push next instruction to stack
        self.reg[0] = self.pc + 2
        self._push(0)
        self.reg[0] = reg0  # put old reg value back in register
        # jump to call site
        self.pc = self.reg[adr]

    def _ret(self):
        reg0 = self.reg[0]
        self._pop(0)
        self.pc = self.reg[0]
        self.reg[0] = reg0



