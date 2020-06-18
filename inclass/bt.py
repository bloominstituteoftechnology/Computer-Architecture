# Branch Tables
# (AKA Dispatch Tables)

def fun1():
    print("fun1")

def fun2():
    print("fun2")

def fun3():
    print("fun3")

def fun4():
    print("fun4")

def call_fun(n):
    branch_table = {
        1 : fun1,
        2 : fun2,
        3 : fun3,
        4 : fun4,
    }
    f = branch_table[n]
    f()


