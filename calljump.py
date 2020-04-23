def fun1(a):
    print("fun1", a)
    
def fun2(a):
    print("fun2", a)
def fun3(a):
    print("fun3", a)
def fun4(a):
    print("fun4", a)

def call_fun(n, a):
#     if n == 1:
#         fun1()
#     elif n ==2:
#         fun2()
#     elif n ==3:
#         fun3()
#     elif n ==4:
#         fun4()
    branch_table = {
        1: fun1,
        2: fun2,
        3: fun3,
        4: fun4
    }

    f = branch_table[n]
    f(a)
call_fun(2, "hello")
call_fun(4, "byE!")
call_fun(1, "hello")