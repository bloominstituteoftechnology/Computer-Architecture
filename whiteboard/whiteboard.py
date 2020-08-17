"""
Implement functionality to reverse an input string. Print out the reversed string.
For example, given a string "cool", print out the string "looc".
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving 
framework while going through your thought process. (edited) 
"""

def rev_string():

    input_string = input("Please Enter A String: ")

    x = [s.lower() for s in input_string]

    x = x[::-1]

    s = ""
    x = s.join(x)

    return x

if __name__ == "__main__":

    # my_string = "Aaron"

    print(rev_string())