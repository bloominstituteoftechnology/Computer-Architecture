
PRINT_MIKE = 0b01
HALT = 0b10 # 2
PRINT_NUM = 0b11 # 3
SAVE = 0b100 # 4
PRINT_REG = 0b101 # 5
ADD = 0b110 # 6


memory = [
    PRINT_MIKE,
    PRINT_MIKE,
    PRINT_NUM,
    42,
    SAVE,
    2,  # index of register to save into
    99, # value to save into register
    SAVE,
    3,  # index of register to save into
    1,  # number to save into register
    ADD,
    2, # index of register to get value
    3, # index of register to get value
    PRINT_REG,
    2,
    HALT,
]

registers = [0] * 8

# Write a program to pull each command out of memory and execute

pc = 0
running = True
while running:
    command = memory[pc]

    if command is PRINT_MIKE:
        print("Mike!")

    if command is HALT:
        running = False

    if command is PRINT_NUM:
        num_to_print = memory[pc + 1]
        print(num_to_print)
        pc += 1

    if command is SAVE:
        reg = memory[pc + 1]
        num_to_save = memory[pc + 2]
        registers[reg] = num_to_save
        pc += 2

    if command is PRINT_REG:
        reg_to_print = memory[pc + 1]
        print(registers[reg_to_print])
        pc += 1
    
    if command is ADD:
        first_reg = memory[pc + 1]
        second_reg = memory[pc + 2]
        
        registers[first_reg] = registers[first_reg] + registers[second_reg]
        pc += 2

    pc += 1

def high_and_low(numbers):
    # ...
    # numbers = numbers.split()
    nums = [int(num) for num in numbers.split()]
    return " ".join([str(max(nums)), str(min(nums))])
    # highest = max(nums)
    # lowest = min(nums)
    # return ", ".join([str(lowest), str(highest)])

x = high_and_low("4 5 29 54 4 0 -214 542 -64 1 -3 6 -6")
print(f"This is x: {x}")

def digital_root(n):
    # ...
    # nums = [num for num in str(n)]
    # print(nums)
    # print(f"This is nums: {nums}")
    from functools import reduce
    print(f"This is n: {n} ")
    if len(str(n)) is 1:
        return n
    return digital_root(reduce(lambda x, y: int(x) + int(y), [num for num in str(n)]))
    # print(f"Length: {len(str(n))}")
    
    
    # digital_root(result)
    
    # return result
    # return reduce(lambda x, y: int(x) + int(y), [num for num in str(n)])
x = digital_root(954)

print(f"This is x: {x}")

roman_numerals = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000
}
# "XXI" = 21
# "MMVIII" = 2008
string_roman = ""
def convert_to_decimal(roman_numeral):
    counted_set = {}
    for c in roman_numeral:
        if c not in counted_set:
            counted_set.setdefault(c, 1)
        else:
            counted_set[c] += 1
    print(counted_set)
    total = 0
    for key in counted_set.keys(): 
        value = roman_numerals[key] * counted_set[key]
        total = total + value
    return total 
y = convert_to_decimal("MMVIII")
# y = bin(int(x[:8]))

print(f"This is y: {y}")

def convert_to_decimal2(roman_numeral):
    roman_numerals = {"I": 1, "IV": 4, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    my_list = [c for c in roman_numeral]
    total = 0
    for i in range(len(my_list[::-1]) - 1):
        if roman_numerals[my_list[i]] < roman_numerals[my_list[i + 1]]:
            total -= roman_numerals[my_list[i]]
        else:
            total += roman_numerals[my_list[i]]
    total += roman_numerals[my_list[-1]]
    return total 
    
x = convert_to_decimal2("IX")
print(f"This is x: {x}")

jaden = "How can mirrors be real if our eyes aren't real"

def jaden_case(string):
    return " ".join([w[0].upper() + w[1:] for w in string.split()])

x = jaden_case(jaden)
print(f"This is x: {x}")

def find_even_index(arr):
    for i in range(1, len(arr)):
        print(f"Front array: {sum(arr[:i + 1])}")
        print(f"Back array: {sum(arr[i + 1:])}")
        if sum(arr[:i]) is sum(arr[i:]):
            return i + 1

x = find_even_index([1,2,3,4,3,2,1])
print(f"This is x: {x}")