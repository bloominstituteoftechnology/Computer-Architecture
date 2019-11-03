print_a = 0b01
halt = 0b10
print_num = 0b11,
memory = [
    print_a,
    print_num,
    0b101,

    print_a,
    print_a,
    halt
]
pc = 0
running = True

while running:

    command = memory[pc]
    if command == print_a:
        print("arp")
        pc+=1
        print("I am pc", pc)
    elif command==print_num:
        num=memory[pc+1]
        print("I am pc",pc)
        print(num)
        pc+=2
        print("I am pc",pc)


    elif command==halt:
        print("pls halt")
        running=False
    else:
        print("don't know")
        running=False

