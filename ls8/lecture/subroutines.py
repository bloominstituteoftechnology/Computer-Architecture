def foo():  
    print(1)  

def bar():  
    print(2)  
    foo()  
    print(3)  

bar()  

foo()  

print('Done')  
"""
When we call:
    1. Push the return address (the address diretly after CALL) on the stack
    2. Set the PC to the address of the subroutine
When we return:
    1. Pop the return address off the stack 
    2. Set PC to the return address, aka, the one just popped off the stack

Stack going downwards
-----------------
            (pc at 9)
push 11     
            (pc at 5)
            (pc at 6) 
push 7      
            (pc at 2)
pop 7        
            (pc at 7)
pop 11      
            (pc at 11)
push 13  
            (pc at 2)
pop 13      
            (pc at 13)

-----------------------
"""
