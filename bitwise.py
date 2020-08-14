OPeration       Boolean OPeration               BitWise OPeration   

AND                     &                               &

    0b10000011
    0b01010101




    test = 0b0010110
    test_buddy = 0b0011001


    #Sometimes people will use a byte of a variable in their projects to represent their id or their truthfullness
    #Bitwise can sometimes be faster rather than  using a bitwise op


    #djB2 hash >> 
    
    0b10101010 >> # bit shifting  is like deleting bits, depending on th amount you shift it by

                    #Adding zeros to the left of the first instance of one does, nothing



    # So what would happen if i only want a select few number inside of a byte. 
    #


    BiTMasking

    0b10101010
    0b00000011 

    # By and'ing these two numbers together you can expose what you really want to know


    #So rightshifting vcauses the n=binaty to move over from the left. 


    0b101000100000       << # We just add zeros . 
    0b00001010   >>


    ADD = 0b10100000


    num_of_ops = ADD >> 6

    alu_operation = (ADD >> 5)  & 0b1




    Masking # We will take adv of how and works 

    # We only want these numbers that wil be in the middle

    ADD = register1 + register2 #ADD takes these two registers as args .

    # How much will the pc jump forward

    pc +=  number_of_operands
    
    
    






    
