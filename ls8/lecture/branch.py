# branch tables
# dispatch tables

def fun1(x, y):
    print(f"fun1 {x}, {y}")

def fun2(x, y):
    print(f"fun2 {x}, {y}")

def fun3(x, y):
    print(f"fun3 {x}, {y}")

def call_fun(n, x=None, y=None):
    branch_table = {
        1:fun1,
        2:fun2,
        3:fun3,
        4:lambda x, y: print(f"lambda {x} {y}")
    }
    # f = branch_table[n]
    # f(x, y)
    branch_table[n](x,y)

call_fun(1, 99,1)
call_fun(2)
call_fun(4, 0, 1)
