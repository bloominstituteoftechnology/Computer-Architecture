import sys
PRINT_BEEJ     = 1  # 0000 0001
HALT           = 2  # 0000 0010
PRINT_NUM      = 3
SAVE           = 4  # Saves a value to a register
PRINT_REGISTER = 5
ADD            = 6

memory = [
  PRINT_BEEJ,
  SAVE,  # Saves the value 65 to register 2
  65,
  2,
  SAVE,  # Saves the value 20 to register 3
  20,
  3,
  ADD,  # ADD the values in r2 += r3
  2,
  3,
  PRINT_REGISTER,  # Print the value in r2
  2,
  PRINT_BEEJ,
  PRINT_BEEJ,
  PRINT_BEEJ,
  HALT,
]
register = [0] * 8

pc = 0
running = True
while running:
    # Execute instructions in memory
    command = memory[pc]
    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc+1]
        print(num)
        pc += 2
    elif command == HALT:
        running = False
        pc += 1
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2
    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)