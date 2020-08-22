"""CPU functionality."""
import sys
sys.path.insert(0, "/Users/jing/Documents/git-repositories/python-practice/Computer-Architecture/ls8/examples/")

# import the binary operation code
from opcodes import OPCODES

# get format as: {'ADD': '10100000', 'AND': '10101000', 'CALL': '01010000', ...}
op_bits = {a: b["code"] for a, b in OPCODES.items()}
# swtich so key is the opcode, value is the readable func name
bits_op = {a:b for b, a in op_bits.items()}

# define flag states:
flag_L = 0b00000100 # less than is true, 4
flag_G = 0b00000010  # greater than than is true, 2
flag_E = 0b00000001  # equal to is true , 1

class CPU:
    def __init__(self):
        """ Initial CPU states when LS-8 is created. This is a 8 bits CPU with 8 wires"""
        # 256 bytes of memory # this holds data that CPU will process
        self.ram = [0]*256  

        # 8 general-purpose registers 
        self.register = [0]*8 

        # internal register:
        # SP: stack pointer is in register[7], but the stack is always in RAM, the start of the stack is F4 hexadecimal
        self.SP = int(0xF4)  # integers in stack address range
        self.register[7] = self.SP 

        self.PC = 0 # program counter, integer to point to lines of code, from first line to last line of current program to run

        self.FL = 0 # flag register
        self.running = True  # cpu running status        
    
    def ram_read(self, addr):
        # read RAM at given address
        return self.ram[addr]

    def ram_write(self, addr, value):
        # write value to ram address
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
                    # store line of code in the computer memeory, aka, ram
                    self.ram_write(address, x)
                    address += 1
            machine_codes = self.ram[:address]
            print(machine_codes)
            print(f"Lines of code = {len(machine_codes)}")

        except FileNotFoundError:
            print("File not found.")
            sys.exit(2) # error exit

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: {self.PC:>02} | {self.ram_read(self.PC):>08b} {self.ram_read(self.PC)+1:>08b} {self.ram_read(self.PC)+2:>08b} |", end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')
        print()

    """ALU operations. Arithmetic and logic operator unit."""   
    def ADD(self, operand_a, operand_b):
        self.register[operand_a] += self.register[operand_b]

    def SUB(self, operand_a, operand_b):
        self.register[operand_a] -= self.register[operand_b]

    def MUL(self, operand_a, operand_b):
        self.register[operand_a] *= self.register[operand_b]

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

    def SHR(self, operand_a, operand_b): # shift to right
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

    """ Other CPU operations """      
    def LDI(self, operand_a, operand_b):
        # load immediately, put a value in a register
        self.register[operand_a] = operand_b        

    def PRN(self, operand_a):
        # print the value in register given address
        print(self.register[operand_a])

    def HLT(self):
        # halt the cpu
        self.running = False
        #sys.exit(0) # python clean exit 
    
    def PUSH(self, operand_a):
        # push the value in the given register on the stack
        # decrement SP, since the stack grows downwards in RAM
        self.SP -= 1
        # get the value from the register
        push_value = self.register[operand_a]
        # store it at the stack pointer
        self.ram_write(self.SP, push_value)
     
    def POP(self, operand_a):
        # pop the value at the top of the stack (SP) into the given register        
        pop_value = self.ram_read(self.SP)
        self.register[operand_a] = pop_value
        # increment SP
        self.SP += 1

    def CALL(self, operand_a):
        # calls the subroutine at the address stored in the register[operand_a]
        # get the value at return address (the one after subroutine_addr) 
        PC_return_addr = self.PC + 2        
        # push it to stack
        self.SP -= 1        
        self.ram_write(self.SP, PC_return_addr)                
        # set the pc to the subroutine address
        self.PC = self.register[operand_a]    

    def RET(self):
        # return from subroutine 
        # pop the top of stack and store it in pc 
        pop_value = self.ram_read(self.SP)
        self.PC = pop_value
        # increment SP
        self.SP += 1    

    def IRET(self):
        # return from an interrupt handler
        # Registers R6-R0 are popped off the stack in that order.
        for i in range(6,-1,-1):
            self.POP(self.register[i])
        # The FL register is popped off the stack.
        self.POP(self.FL)
        # The return address is popped off the stack and stored in PC.
        self.POP(self.PC)        
    
    def JMP(self, operand_a):
        # jump to address given
        self.PC = self.register[operand_a]
    
    def JEQ(self, operand_a):
        # jump if is equal flag is true 
        if self.FL == flag_E:
            self.PC = self.register[operand_a]
        else:
            self.PC += 2
    
    def JNE(self, operand_a):
        # jump if not equal to
        if self.FL != flag_E:
            self.PC = self.register[operand_a]
        else:
            self.PC += 2

    def fun_map(self, fun):
        # to call cpu subroutines using a branch table
        branch_table = {
            "LDI": self.LDI,
            "PRN": self.PRN,
            "HLT": self.HLT,
            "POP": self.POP,
            "PUSH": self.PUSH,
            "CALL": self.CALL,
            "RET": self.RET,
            # ALU opeators 
            "ADD": self.ADD,
            "SUB": self.SUB,
            "AND": self.AND,
            "OR" : self.OR, 
            "XOR": self.XOR,
            "NOT": self.NOT,
            "MUL": self.MUL,
            "SHL": self.SHL,
            "SHR": self.SHR,
            "MOD": self.MOD,
            # following are added for sprint challenge
            "CMP": self.CMP,
            "JMP": self.JMP,
            "JEQ": self.JEQ,
            "JNE": self.JNE,
        }
        # return the function        
        return branch_table[fun]
        
        
    def run(self):
        """Run the CPU."""
        while self.running:  
            
            # read address in register PC and store it in Instruction register (IR)  
            # breakpoint()
            IR = self.ram_read(self.PC) 
            # remove 0b infront of bits and fill left with zero
            IR = bin(IR)[2:].zfill(8)
           
            if IR in bits_op:
                # self.trace()
                # get the readable function 
                IR_readable = bits_op[IR]
                # fun = getattr(self, IR_readable.lower())
                # # return the number of operands:
                # sig = signature(fun)
                # N_operands = len(str(sig))-1
                
                # To find the number of operands,
                # mask for the first two bits, shift right by 6
                num_operands = (int(op_bits[IR_readable], 2) & 0b11000000) >> 6
                # print(f"number of operands {num_operands}")
                operand_a = self.ram_read(self.PC + 1)
                operand_b = self.ram_read(self.PC + 2)

                operation = self.fun_map(IR_readable)

                # print(f"Operation {IR_readable} {operand_a} {operand_b}")
                # call the function accordingly on number of operands
                if num_operands == 0:                    
                    operation()

                elif num_operands == 1:
                    operation(operand_a)

                else:
                    # num_operands == 2:
                    operation(operand_a, operand_b)
                
                # check if the instruction set the PC
                set_PC = (int(op_bits[IR_readable], 2) & 0b00010000) >> 4
                
                # set_PC=1 means the operation set PC by itself
                if set_PC == 0:
                    # manually set the PC after the operation 
                    self.PC += (num_operands + 1)
                # print(f"setPC is {set_PC}")           
            else:
                print(f"unknow instruction {self.ram_read(self.PC)} at PC address {self.PC}")
                sys.exit(1)

            
if __name__=="__main__":
    cpu = CPU()
    cpu.load()
    cpu.run()
