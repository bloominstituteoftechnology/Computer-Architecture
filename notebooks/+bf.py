def foo():
    print("foo")


bar = foo
baz = foo
frotz = bar

foo()
bar()
baz()
frotz()
