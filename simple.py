# This is our assembly library
Print_yaya =    0b00000001
Halt =          0b00000010
print_num =     0b00000011 # commmand 3
Save =          0b00000111
Print_Register = 0b00000101
ADD         =   0b00000110

memory = [Print_yaya, Print_yaya,print_num,99, SAVE, 42, 2,ADD, 42, SAVE,42, 3,ADD, 2, 3, Print_Register,2, Halt]

#We want the computer to iterate through mem
# For loop OR While loop
# THe computer will send an address in RAM. 


#Memory BUS 
#A bunch of wires that the cpy uses to send an address to ram
#THere is also a data bus this is what ram sends back to the cpu
        """
        CPU
       ||||||||
       ||||||||
       ||||||||
       ||||||||
        RAM 

        This represents the wires seperating the cpu from ram

        Each wire that is firing will identify where  in memory it is in terms of the address 




        """

running = True
counter = 0

#REGISTERS ( Use them as variables)
#R0 - R7

registers = [None] *  8
while running:                          #This is like an interpreter ---> A program that that prints programs.
                                        #The purpose of this program is to replicate a computers processes  in an abstracted way
                                        #Registers act as easy to access =points of memor
                                        #Memory holds bits inside of an array like structure. 

    command = memory[counter] #Command is peaking at what is the current index in memory

    if command == Print_yaya:
        print("Yaya")

        counter += 1

    if command == print_num: 
        ans   = memory[counter +1 ]
        print(ans) 

        counter += 2

    if command == SAVE: 
        ans_save = memory[counter + 1 ]
        index = memory[counter + 2 ]
        registers[index] = ans_save



    if command == Print_Register:
        reg_index = memory[pc + 1]
        print(registers[reg_index])
        counter += 2

    if command == ADD: 
        first_reg_idx = memory[pc + 1]
        secon_reg_idx  = memory[pc + 2]

    if command == Halt:
        running = False
        #Or you could use sys.exit
        #WHat is sys exit'


        #The goal is to be able to read a file that is  showing the commnds
            #This will be done with file open pyton method
            #After every command is read then then we will tell the counter to increment based on the 
            #Amount of space the command took.