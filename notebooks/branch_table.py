# Branch Tables
# (AKA Dispatch Tables)


def fun1(x, y):
    print(f"fun1 {x} {y}")


def fun2(x, y):
    print(f"fun2 {x} {y}")


def fun3(x, y):
    print(f"fun3 {x} {y}")


def fun4(x, y):
    print(f"fun4 {x} {y}")


def call_fun(n, x=None, y=None):
    """
    if n == 1:
            fun1(x, y)
    elif n == 2:
            fun2(x, y)
    elif n == 3:
            fun3(x, y)
    elif n == 4:
            fun4(x, y)
    """

    branch_table = {
        1: fun1,
        2: fun2,
        3: fun3,
        4: fun4,
        5: lambda x, y: print(f"lambda {x} {y}")
    }

    #f = branch_table[n]
    #f(x, y)
    branch_table[n](x, y)


call_fun(2, 99, 100)
call_fun(3, 2, 3)
call_fun(5, 33, 44)
