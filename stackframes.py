# Stack frames
# STack grows downward:
#
# 701:
# 700: return point 1 |
# 699: a = 2          | main()'s stack frame
# 698: b = ??         |

# 697: return point 2 |\
# 696: x =  2         | mult2
# 695: y =  7         |     stack
# 694: z = 14         |         frame

# z value will temporarily get stored in the register like R0
'''
When you call, return addr gets pushed on the stack
When you return, return gets popped off the stack and store it into PC
'''
def mult2(x, y):
    z = x * y
    return z
 

def main():
    a = 2

    b = mult2(a, 7)
    # return point 2
    print(b)
    return

main()
# return point 1
print("Done!")