"""CPU functionality."""

import sys

## KEY
# * `iiiiiiii`: 8-bit immediate value
# * `00000rrr`: Register number
# * `00000aaa`: Register number
# * `00000bbb`: Register number


## Establishing acronyms for all programs to be used in cpu.py
""" Primary Programs """
LDI = 0b10000010    ## Load Immediate - store value in register, set register to this value
LD = 0b10000011     ## Load from Other - Loads RegA with value at the memory address stored in Register B
PRN = 0b01000111    ## Print numeric value stored in register
HLT = 0b00000001    ## Halt. Stops CPU and exits emulator
POP = 0b01000110    ## Pop.
PUSH = 0b01000101   ## Push.
NOP = 0b00000000    ## No OPeration. Pass
CALL = 0b01010000   ## Calls specific subroutine (a function/program) at an address
# 01010000 00000rrr // This is address. After sending it call(address), the PC moves to the location in RAM and executes that program.
RET = 0b00010001    ## Return. 

""" Mathy Programs """
INC = 0b01100101    ## Increment (add 1) to value of the passed register
## 01100101 00000rrr
DEC = 0b01100110    ## Decrement (subtract 1 from) a value in the passed register
## 01100110 00000rrr // value
ADD = 0b10100000    ## Add. Add two registers, and replace RegA with the sum
# 10100000 00000aaa 00000bbb
SUB = 0b10100001    ## Subtract. Put result in RegA
MUL = 0b10100010   ## Multiply. Multiplies two Registers together.
DIV = 0b10100011    ## Divide. RegA/RegB. Result is stored as RegA. Exit case of RegB == 0, then HLT
## 10100011 00000aaa 00000bbb
MOD = 0b10100100    ## Remainder. Divide RegA/ReB, place the remainder in RegA. Exit Case of RegB == 0, then HLT

""" Comparison Programs """
AND = 0b10101000    ## And. The Bitwise AND ( & ). 
NOT = 0b01101001    ## Not. The Bitwise-NOT. Uses 1 Register. Stores result in that register
OR = 0b10101010     ## Or, can be Both. The Bitwise-OR. 2 Registers.
XOR = 0b10101011    ## One OR the Other, not Both.
## Comp Graphs
# A B   AND  OR  XOR  NOR  NAND
# 0 0    0   0    0    1    1
# 0 1    0   1    1    0    1
# 1 0    0   1    1    0    1
# 1 1    1   1    0    0    0

CMP = 0b10100111    ## Comparison(rega, regb). Compares two things and returns a value based upon it. Changes specific FL based it. Flag 'E' ==, sets to 1, Flag 'L' RegA < ReB sets to 1, Flag 'G' RegA > RegB sets to 1
## 10100111 00000aaa 00000bbb, A7 0a 0b


""" ????????? """
INT = 0b01010010    ## Interrupt ??????????????????
      # Issue the interrupt number stored in the given register.

      # This will set the _n_th bit in the `IS` register to the value in the given
      # register.

      # Machine code:
      # ```
      # 01010010 00000rrr
IRET = 0b00010011   ## Return from Interrupt


""" Jump Statements """
JMP = 0b01010100    ## Jump to address in the register. Set PC to that address
# Jump to an address in register if the noted Flags (FL) are set to True (1)
JNE = 0b10000011    ## Jump if Not Equal
JEQ = 0b01010101    ## Jump if Equal
JGE = 0b01011010    ## Jump if Greater/Equal
JGT = 0b01010111    ## Jump if Greater Than
JLE = 0b01011001    ## Jump if Less/Equal
JLT = 0b01011000    ## Jump if Less Than


""" Other Acronyms """
## Basic Acronyms
# CPU = Central Processing Unit
# ALU = Arithmetic-Logic Unit, carries out maths and logic operations

## Internal Registers
# IR = Instruction Register - address of currently running instruction
# MAR = Memory Address Register - Holds Memory Address we're reading/writing
# MDR = Memory Data Register - Holds value to write/Value just read
# FL = Flags (current Flags: E, L, G)


class CPU:
  """Main CPU class."""

  def __init__(self):
    """Construct a new CPU."""
    self.pc = 0
    self.ram = [0] * 256
    self.reg = [0] * 8
    self.usage = 0
    self.sp = 7
    self.fl = 0b00000000

  def ram_read(self, MAR):
    # print('we in ram_read')
    return self.ram[MAR]
  
  def ram_write(self, MAR, MDR):
    self.ram[MAR] = MDR
    return self.ram[MAR]


  def load(self, file):
    """Load a program into memory."""
    file = file
    address = 0

    with open(file) as f:
      for line in f:
        n = line.split('#')
        n[0] = n[0].strip()
        if n[0] == '':
          continue
        value = int(n[0], 2)
        self.ram[address] = value
        address += 1
        self.usage += 1


    print(f"self.ram : {self.ram}")

  def alu(self, operation, reg_a, reg_b):
    """ALU operations."""

    if operation == "ADD":
      self.reg[reg_a] += self.reg[reg_b]
    elif operation == "MUL":
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

  ## Cheaty way
  # new function called run_notmathy(ir, op_aa, op_b)
  # Move the if else loop here

  def run(self):
    """Run the CPU."""
    running = True
    print('HERE BE DA RAM', self.ram)
    
    while running:
      # print('before ir')
      ir = self.ram_read(self.pc)
      # print('before reg_a')
      reg_a = self.ram_read(self.pc + 1)
      # print('before reg_b')
      reg_b = self.ram_read(self.pc + 2)

      ## checking if mathy or logicy
      # isalu =
      ## operator = 0b10101111
      ## check = 0b0010000
      ## True
      # ? shift >> 5 spots?



      ### have if statement that checks if isalu is true. If so it calls the alu and pass the appropriate arguments
      ## Then shift the opccode => into a dictionary.


      if ir == HLT:
        print("STOP, IT'S DA POLICE")
        running = False

      if ir == LDI:
        print("Loading value from reg")
        self.reg[reg_a] = reg_b
        self.pc += 3

      elif ir == PRN:
        print("Printing our stuff")
        print(self.reg[reg_a])
        self.pc += 2

      elif ir == MUL:
        print("Multiplying RegA vs RegB", reg_a, reg_b, reg[reg_a], reg[reg_b])
        print(self.reg[reg_a]*self.reg[reg_b])
        self.pc += 3

      elif ir == PUSH:
        print("Push onto stack")
        self.reg[self.sp] -= 1
        value = self.reg[reg_a]
        self.ram[self.reg[self.sp]] = value
        self.pc += 2

      elif ir == POP:
        print("What's poppin'")
        value = self.ram[self.reg[self.sp]]
        self.reg[reg_a] = value
        self.reg[self.sp] += 1
        self.pc += 2

      elif ir == CALL:
        print("Calling to new location")
        return_address = self.pc + 2
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = return_address

        reg_num = self.ram[self.pc + 1]
        sub_address = self.reg[reg_num]
        self.pc = sub_address

      elif ir == RET:
        print("Returning to previous address")
        return_address = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc = return_address

      elif ir == ADD:
        print("Add some stuff", self.reg[reg_a], self.reg[reg_b])
        value = self.reg[reg_a] + self.reg[reg_b]
        self.reg[reg_a] = value
        self.pc += 3

      else:
          print(f"Don't know what's going on here at: {self.pc}")