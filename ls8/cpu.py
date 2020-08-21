"""CPU functionality."""
import sys
# from inspect import signature
sys.path.insert(
    0, "/Users/jing/Documents/git-repositories/python-practice/Computer-Architecture/ls8/examples/")
# import the binary operation code
from opcodes import OPCODES
# op_bits = {'ADD': '10100000', 'AND': '10101000', 'CALL': '01010000', ...}"""
op_bits = {a: b["code"] for a, b in OPCODES.items()}
# swtich so key is the opcode, value is the readable func name
bits_op = {a:b for b, a in op_bits.items()}

# define flag states:
flag_L = 0b00000100 # less than is true
flag_G = 0b00000010  # greater than than is true
flag_E = 0b00000001  # equal to is true

class CPU:
    """Main CPU class."""
    def __init__(self):
        """ CPU states when LS-8 is created
        this is a 8 bits CPU with 8 wires"""
        # 256 bytes of memory # this holds data that CPU will process
        self.ram = [0]*256  
        # 8 general-purpose registers 
        self.register = [0]*8 
        # internal register:
        # SP: stack pointer is in register[7], but the stack is always in RAM, the start of the stack is F4 hexadecimal
        self.SP = int(0xF4) 
        self.register[7] = self.SP

        self.PC = 0 # internal register for program counter
        self.FL = 0 # flag register
        self.running = True  # cpu running status        
    
    def ram_read(self, addr):
        # read RAM 
        return self.ram[addr]

    def ram_write(self, addr, value):
        # write value to ram
        self.ram[addr] = value
    
    def load(self):
        """Load a program into memory. 
        Open a program file, read its contents and 
        save appropriate data into RAM"""
        address = 0 # for temporary load program
        # read program file 
        #filename = "./examples/mult.ls8"
        filename = sys.argv[1]
        try:
            with open(filename) as f:
                # print([b for a, b in enumerate(f)])
                for line in f:
                    line = line.split("#")                
                    try:
                        x = int(line[0], 2)  # base 10 number
                        # print(x)
                    except ValueError:
                        continue
                    # store file content in ram
                    self.ram_write(address, x)
                    address += 1
        except FileNotFoundError:
            print("File not found.")
            sys.exit(2) # error exit

    """ALU operations. Arithmetic and logic operator unit."""   

    def ADD(self, operand_a, operand_b):
        self.register[operand_a] += self.register[operand_b]

    def SUB(self, operand_a, operand_b):
        self.register[operand_a] -= self.register[operand_b]

    def AND(self, operand_a, operand_b):
        self.register[operand_a] &= self.register[operand_b]

    def OR(self, operand_a, operand_b):
        self.register[operand_a] |= self.register[operand_b]

    def XOR(self, operand_a, operand_b):
        self.register[operand_a] ^= self.register[operand_b]

    def NOT(self, operand_a, operand_b):
        self.register[operand_a] != self.register[operand_b]

    def SHL(self, operand_a, operand_b): # shift to left
        self.register[operand_a] <<= self.register[operand_b]

    def SHR(self, operand_a, operand_b):
        self.register[operand_a] >>= self.register[operand_b]

    def MOD(self, operand_a, operand_b):
        if self.register[operand_b] == 0:
            print('MOD encounters division by zero!')
            self.running = 0
            sys.exit(1)
        else:            
            self.register[operand_a] %= self.register[operand_b]     

    def CMP(self, operand_a, operand_b):
        #  Compare two operands, and set the flag register 
        if self.register[operand_a] < self.register[operand_b]:
            self.FL = flag_L
        elif self.register[operand_a] > self.register[operand_b]:
            self.FL = flag_G   
        elif self.register[operand_a] == self.register[operand_b]:
            self.FL = flag_E          
        else:
            self.FL = 0
        
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')
        print()
    
    def ldi(self, operand_a, operand_b):
        # load immediately, store a value in a register
        self.register[operand_a] = operand_b        

    def prn(self, operand_a):
        # print a value stored in a register
        print(self.register[operand_a])

    def hlt(self):
        # halt the cpu
        self.running = False
        #sys.exit(0) # exit python

    def mul(self, operand_a, operand_b):
        self.register[operand_a] *= self.register[operand_b]
    
    def push(self, value):
        # decrement SP
        self.register[self.SP] -=1
        reg_num = self.ram[self.PC+1]
        # get the value from the register
        value = self.ram_read([reg_num])
        # store it at the stack pointer
        self.ram_write(self.register[self.SP], value)
     
    def pop(self, operand):
        # get the value from the SP, write to ram at address operand
        top_of_stack_addr = self.register[self.SP]
        value = self.ram_read(top_of_stack_addr)
        self.ram_write(operand, value)
        # increment SP
        self.register[self.SP] += 1

    def call(self, subroutine_addr):
        # push the return address to stack
        return_addr = self.ram_read(self.PC+2)        
        self.push(return_addr)         
        # set the pc to the subroutine address 
        self.PC = subroutine_addr

    def ret(self):
        # return from subroutine 
        # pop the top of stack and set pc at that value
        return_addr = self.ram_read(self.SP)
        self.PC = self.reg[return_addr]
    
    def jmp(self, reg_addr):
        # jump to address given
        self.PC = self.register[reg_addr]
    
    def jeq(self, reg_addr):
        # jump if is equal flag is true 
        if self.FL == flag_E:
            self.jmp(reg_addr)
    
    def jne(self, reg_addr): 
        # jump if not equal to
        if self.FL == 0:
            self.jmp(reg_addr)

    def fun_map(self, fun):
        # to call cpu subroutines
        branch_table = {
            "LDI": self.ldi,
            "PRN": self.prn,
            "HLT": self.hlt,
            "MUL": self.mul,
            "POP": self.pop,
            "PUSH": self.push,
            "MUL": self.mul,
            "CALL": self.call,
            "RET": self.ret, 
            # following are added for sprint challenge
            #"CMP": self.alu(cmp,
            "JMP": self.jmp,
            "JEQ": self.jeq,
            "JNE": self.jne,
        }
        # return the function
        return branch_table[fun]
        
        
    def run(self):
        """Run the CPU."""
        while self.running:  
            # read address in register PC and store it in IR        
            IR = self.ram_read(self.PC)  # instruction register
            
            
            # get instruction
            if IR in bits_op:
                # get the function 
                IR_readable = bits_op[IR]
                # get the method of IR, ex, self.ldi
                # fun = getattr(self, IR_readable.lower())
                # # return the number of operands:
                # sig = signature(fun)
                # N_operands = len(str(sig))-1
                
                # to find the number of operands,
                # mask for the first two bits, shift right by 6
                num_operands = (op_bits[IR_readable] & 0b11000000) >> 6

                operand_a = self.ram_read(self.PC + 1)
                operand_b = self.ram_read(self.PC + 2)
                
                # call the function accordingly on number of operands
                if num_operands == 0:                    
                    self.fun_map(IR_readable)()

                elif num_operands == 1:
                    self.fun_map(IR_readable)(operand_a)

                elif num_operands == 2:
                    self.fun_map(IR_readable)(operand_a, operand_b)
                
                # set the PC after the operation 
                self.PC += (num_operands + 1)
                           
            else:
                print(f"unknow instruction {IR} at address {self.PC}")
                sys.exit(1)

            
"""         if IR not in op_bits.values():
                print("Instruction not prescribed")
                sys.exit(1)

            if IR == op_bits["LDI"]:
                self.ram_write(operand_a, operand_b)
                self.PC += 3

            elif IR == op_bits["PRN"]:
                print(self.ram_read(operand_a))
                self.PC += 2

            elif IR == op_bits["HLT"]:
                self.running = False
                self.PC += 1
"""


if __name__=="__main__":
    cpu = CPU()
    cpu.load()
    cpu.run()
