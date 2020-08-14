import sys
print(sys.argv)


if len(sys.argv) < 2: 
    print("did you forget the file to open")
    print('Usage: filename file_to_open')
    sys.exit()
try:

    with open(sys.argv[1]) as file:  
        for line in file: 
            comment_split = line.split('#')

            possible_num = comment_split[0]

            if possible_num[0] == '1' or possible_num[0] == '0':

            print(comment_split)


except FileNotFoundError:  
    print(f'{sys.argv[0]}: {sys.argv[1]} not found')

"""
try: 

    file = open('ls8.py', 'r')
    lines = file.read()
    print(lines)

except Exception: 
    print(file.closed) 

try: 
    with open('examples/print.ls8') as file: 
        for line in file: 
            print(line)
            raise Exception("hi")

except Exception: 
    print(file.closed)

    """


    #So we are opening a file that will have our commands in a list
    #All we have to do is set  up the iteration parameters. 
    #Bro all i have is just 4 months!
    

     


    