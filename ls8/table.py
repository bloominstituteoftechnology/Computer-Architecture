'''
Branchtable for O(1) access to instruction functions
'''
class Branchtable():
    def __init__(self, cpu):
        self.branchtable = {}

        # instructions
        self.branchtable[0x01] = self.hlt
        self.branchtable[0x82] = self.ldi
        self.branchtable[0x47] = self.prn
        self.branchtable[0xA2] = self.mul
        self.branchtable[0x46] = self.pop
        self.branchtable[0x45] = self.push
        self.branchtable[0x50] = self.call
        self.branchtable[0x11] = self.ret
        self.branchtable[0xA0] = self.add
 
        # use reference to cpu class to make updates
        self.cpu = cpu

    def hlt(self, *args):
        '''
        stops prgram by setting halt flag to true
        '''
        self.cpu.halt = True

    def ldi(self, *args):
        '''
        sets the value of a register to a specified integer value
        '''
        r = args[0]
        value = args[1]
        self.cpu.reg[r] = value

    def prn(self, *args):
        '''
        Print value at stored in specified register
        '''
        r = args[0]
        print(self.cpu.reg[r])

    def mul(self, *args):
        '''
        Multiply values passed in registers
        '''
        op = 'MUL'
        r_a = args[0]
        r_b = args[1]
        self.cpu.alu(op, r_a, r_b)

    def add(self, *args):
        '''
        Adds values passed in registers
        '''
        op = 'ADD'
        r_a = args[0]
        r_b = args[1]
        self.cpu.alu(op, r_a, r_b)
    
    def pop(self, *args):
        '''
        Reads item off top of stack into register
        Increments the stack pointer
        '''
        r = args[0]

        if self.cpu.sp != 0xF4:
            self.cpu.reg[r] = self.cpu.ram_read(self.cpu.sp)
            self.cpu.sp += 1
        else:
            raise Exception('Empty stack')

    def push(self, *args):
        '''
        Writes item onto stack from given register
        Decrements the stack pointer
        '''
        r = args[0]
        self.cpu.sp -= 1
        self.cpu.ram_write(self.cpu.sp, self.cpu.reg[r])

    def call(self, *args):
        '''
        Loads next instruction onto stack, then sets the 
        program counter to value stored in reg
        '''
        r = args[0]
        self.cpu.reg[4] = self.cpu.pc + 2
        self.push(4)
        self.cpu.pc = self.cpu.reg[r] 

    def ret(self, *args):
        '''
        sets the program counter to previous location
        first loading into reg 4 and from there to pc
        '''
        self.pop(4)
        self.cpu.pc = self.cpu.reg[4]

    def contains(self, instruction):
        if instruction in self.branchtable:
            return True
        else:
            return False

    def instruction(self, instruction):
        return self.branchtable[instruction]


