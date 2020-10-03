def genInt(str):
    """
    genByte takes an 8 digit binary string and returns a the integer representation
    e.g. '00001000' returns 8
    """
    dig_map = {
        1: 128,
        2: 64,
        3: 32,
        4: 16,
        5: 8,
        6: 4,
        7: 2,
        8: 1
    }
    
    # Validate the input string length
    if len(str) != 8:
        print("ERR: input string does not have a length of 8")
        return
    
    # Convert the string to a binary representation
    num = 0
    ctr = 1
    for chr in str:
        if chr == "1":
            num = num + dig_map[ctr]
        ctr = ctr + 1

    return num