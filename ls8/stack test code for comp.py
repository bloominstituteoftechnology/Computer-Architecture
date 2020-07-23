# Should print out 99

3  # SAVE_REG R0,99
0
99
3  # SAVE_REG R1,33
1
33
5  # PUSH R0
0
5  # PUSH R1
1
6  # POP R2
2
6  # POP R2
2
4  # PRINT_REG R2
2
2  # HALT
