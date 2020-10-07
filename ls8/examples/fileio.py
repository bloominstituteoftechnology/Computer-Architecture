
import sys 
# f = open('print8.ls8', 'r')
# try:
#     lines = f.read()
#     print(lines)
    
#     raise Exception('hi')
# except:
#     print(f.closed)
print(len (sys.argv) )   
if (len(sys.argv)) !=2:
    print('remember to pass the filemname')
    print(' python3 fileio.py <second_file_name.py')
    sys.exit()
    
try:    
    with open (sys.argv[1])   as f:
        for line in f:
           possible_number =  line[:line.find("#")] 
           if possible_number == "":
               continue
           
           
           regular_int = int(possible_number, 2)
           print(regular_int)
             # line = line[:line.find]
except FileNotFoundError:
    print(f'Error from{sys.argv[0]}: {sys.argv[1]} not found') 
    sys.exit()
