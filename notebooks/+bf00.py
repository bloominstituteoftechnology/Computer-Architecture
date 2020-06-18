# Branch Tables
# (AKA) Dispatch Tables)

# def function1():


def function1(x, y):
    # print("function1")
    print(f"function1 {x} {y}")


def function2(x, y):
    # print("function2")
    print(f"function2 {x} {y}")


def function3(x, y):
    # print("function3")
    print(f"function3 {x} {y}")


def function4(x, y):
    # print("function4")
    print(f"function4 {x} {y}")


def call_function(n, x=None, y=None):
    branch_table = {
        1: function1,
        2: function2,
        3: function3,
        4: function4,
        # writen as a lambda function:
        5: lambda x, y: print(f"lambda {x} {y}")
        # if n == 1:
        # function1()
        # elif n == 2:
        # function2()
        # elif n == 3:
        # function3()
        # elif n == 4:
        # function4()

    }
    # f = branch_table[n]
    # f(x, y)
    branch_table[n](x, y)


call_function(2, 99, 100)
call_function(3, 2, 3)
call_function(5, 33, 44)
