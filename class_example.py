PRINT_TIM = 0b00000001
HALT = 0b00000010
PRINT_NUM = 0b00000011  # a 2-byte command, takes 1 argument
SAVE = 0b00000100  # a 3-byte command, takes 2 arguments
PRINT_REG = 0b00000101
PRINT_SUM = 0b00000110
​
​
# a data-driven machine
# function call
# a "variable" == registers for our programs to save things into
​
​
# RAM
memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,   # print 99 or some other number
    42,
    SAVE,  # save 99 into register 2             # <-- PC
    99,    # the number to save
    2,     # the register to put it into
    PRINT_REG,
    2,
    PRINT_SUM,  # R1 + R2
    HALT,
]
​
​
# registers, R0-R7
registers = [0] * 8
​
running = True
​
# program counter
pc = 0
​
while running:
    command = memory[pc]
​
​
if command == PRINT_TIM:
    print('tim!')
​
elif command == PRINT_NUM:
    num_to_print = memory[pc + 1]  # we already incremented PC!
    print(num_to_print)
​
pc += 1   # but increment again
​
​
elif command == SAVE:
    num_to_save = memory[pc + 1]
    register_address = memory[pc + 2]
​
registers[register_address] = num_to_save
​
# shorter:
# registers[memory + 2] = memory[pc + 1]
​
pc += 2
​
elif command == PRINT_REG:
    reg_address = memory[pc + 1]
​
saved_number = registers[reg_address]
​
print(saved_number)
​
# print(registers[memory[pc + 1]])
​
​
elif command == HALT:
    running = False
​
​number
pc += 1  # so we don't get sucked into an infinite loop!

# masking
# >> and use & with ob1 to essentially delete any higher bits
ob1010
&   ob0000
------

0b1010
&   0b0011    zeros where you don't care, ones where you do
------
0b0010

shift to the right, then masking
v

10100000 >> 5
101
00000101

00000101
&00000001
--------
00000001


#  LOADING STUFF
# file i/o in python
try:
    if len(sys.argv) < 2:
        print(f'error from {sys.argv[0]}: {sys.argv[1]} not found')
        sys.exit(1)

    # add a counter that loads memory at that index
    ram_index = 0

    with open(file_name, sys.argv[1]) as f:
        for line in f:
            print(line.split("#")[0])
            print(split_line.strip())
            # how to only get the numbers
            if stripped_split_line != "":
                print(stripped_split_line)
                command = int(stripped_split_line, 2)
                # loead command into memory
                memory[ram_index] = command
                ram_index += 1

except FileNotFoundError:
    print(f"could not find that file {sys.argv[1]}")

file = open("print8.ls8", 'r')
lines = file.read()

print(lines)
# make sure you close files
file.close()

# read in filename from command line

memory = [0] * 256


elif command = ADD:
    reg1_address = memory[pc + 1]
    reg2_address = memory[pc + 2]

    registers[reg1_address] += registers[reg2_address]
