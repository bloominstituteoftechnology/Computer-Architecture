#!/usr/bin/env python3

# Assembler for LS-8 v4.0
#
# Example code:
#
#  INC R0   ; A comment
#  Label1:
#  DEC R2
#  LDI R3,Label1
#
#  DS A String that is declared
#  DB 0x0a   ; a hex byte
#  DB 12   ; a decimal byte
#  DB 0b0001 ; a binary byte

import sys
import re

# Opcodes
OPCODES = {
    "ADD":  {"type": 2, "code": "10100000"},
    "AND":  {"type": 2, "code": "10101000"},
    "CALL": {"type": 1, "code": "01010000"},
    "CMP":  {"type": 2, "code": "10100111"},
    "DEC":  {"type": 1, "code": "01100110"},
    "DIV":  {"type": 2, "code": "10100011"},
    "HLT":  {"type": 0, "code": "00000001"},
    "INC":  {"type": 1, "code": "01100101"},
    "INT":  {"type": 1, "code": "01010010"},
    "IRET": {"type": 0, "code": "00010011"},
    "JEQ":  {"type": 1, "code": "01010101"},
    "JGE":  {"type": 1, "code": "01011010"},
    "JGT":  {"type": 1, "code": "01010111"},
    "JLE":  {"type": 1, "code": "01011001"},
    "JLT":  {"type": 1, "code": "01011000"},
    "JMP":  {"type": 1, "code": "01010100"},
    "JNE":  {"type": 1, "code": "01010110"},
    "LD":   {"type": 2, "code": "10000011"},
    "LDI":  {"type": 8, "code": "10000010"},
    "MOD":  {"type": 2, "code": "10100100"},
    "MUL":  {"type": 2, "code": "10100010"},
    "NOP":  {"type": 0, "code": "00000000"},
    "NOT":  {"type": 1, "code": "01101001"},
    "OR":   {"type": 2, "code": "10101010"},
    "POP":  {"type": 1, "code": "01000110"},
    "PRA":  {"type": 1, "code": "01001000"},
    "PRN":  {"type": 1, "code": "01000111"},
    "PUSH": {"type": 1, "code": "01000101"},
    "RET":  {"type": 0, "code": "00010001"},
    "SHL":  {"type": 2, "code": "10101100"},
    "SHR":  {"type": 2, "code": "10101101"},
    "ST":   {"type": 2, "code": "10000100"},
    "SUB":  {"type": 2, "code": "10100001"},
    "XOR":  {"type": 2, "code": "10101011"},
}

# Regex for matching lines
# Capturing groups: label, opcode, operandA, operandB
REGEX = r"(?:(\w+?):)?\s*(?:(\w+)\s*(?:(\w+)(?:\s*,\s*(\w+))?)?)?"

# Regex for capturing DS and DB data
REGEX_DS = r"(?:(\w+?):)?\s*DS\s*(.+)"  # insensitive
REGEX_DB = r"(?:(\w+?):)?\s*DB\s*(.+)"  # insensitive


def parse_commandline(argv):
    """
    Usage: asm.py [inputfile] [outputfile]
    """

    if len(argv) == 1:
        inputfile = "-"
        outputfile = "-"

    elif len(argv) == 2:
        inputfile = argv[1]
        outputfile = "-"

    elif len(argv) == 3:
        inputfile = argv[1]
        outputfile = argv[2]

    else:
        print("usage: asm.py [infile.asm] [outfile.ls8]", file=sys.stderr)
        sys.exit(1)

    return inputfile, outputfile


def open_files(inputfile, outputfile):
    """
    Open files for reading and writing. If either of the files are named "-",
    stdin or stdout is returned as appropriate.
    """

    if inputfile == "-":
        inputfile = sys.stdin
    else:
        inputfile = open(inputfile)

    if outputfile == "-":
        outputfile = sys.stdout
    else:
        outputfile = open(outputfile, "w")

    return inputfile, outputfile


def normalize_line(groups):
    """
    Takes match groups and uppercases them if they're not None.
    """

    result = []

    for g in groups:
        if g is None:
            result.append(None)
        else:
            result.append(g.upper())

    return result


def p8(v):
    return "{:08b}".format(v)


def pass1(inputfile, sym, code):
    """
    Pass 1

    * Read the source code lines
    * Parse labels, opcodes, and operands
    * Record label offsets
    * Emit machine code
    """

    # Source line number
    line_num = 0

    # Current code address (for labels)
    addr = 0

    def get_reg(op, fatal=True):
        """Get a register number from a string, e.g. "R2" -> 2"""

        nonlocal line_num

        m = re.match(r"R([0-7])", op)

        if m is None:
            if fatal:
                print(r"Line {line_num}: unknown register {op}",
                      file=sys.stderr)
                sys.exit(1)
            else:
                return None

        return int(m.group(1))

    def out0(opcode, op_a, op_b, machine_code):
        """Handle opcodes with zero operands"""

        nonlocal addr

        code.append(f"{machine_code} # {opcode}")
        addr += 1

    def out1(opcode, op_a, op_b, machine_code):
        """Handle opcodes with one operand"""

        nonlocal addr

        reg_a = get_reg(op_a)
        code.append(f"{machine_code} # {opcode} {op_a}")
        code.append(p8(reg_a))
        addr += 2

    def out2(opcode, op_a, op_b, machine_code):
        """Handle opcodes with two operands"""

        nonlocal addr

        reg_a = get_reg(op_a)
        reg_b = get_reg(op_b)

        code.append(f"{machine_code} # {opcode} {op_a},{op_b}")
        code.append(p8(reg_a))
        code.append(p8(reg_b))

        addr += 3

    def out8(opcode, op_a, op_b, machine_code):
        """Handle LDI opcode (type 8)"""

        nonlocal addr

        reg_a = get_reg(op_a)

        try:
            val_b = int(op_b, 0)
            out_b = p8(val_b)

        except ValueError:
            # If it's not a value, it might be a symbol
            out_b = f"sym:{op_b}"

        code.append(f"{machine_code} # {opcode} {op_a},{op_b}")
        code.append(p8(reg_a))
        code.append(out_b)

        addr += 3

    def handle_ds(line):
        """
        Handle DS pseudo-opcode
        """

        nonlocal addr

        m = re.match(REGEX_DS, line, re.IGNORECASE)

        if m is None or m.group(2) is None:
            print(f"line {line_num}: missing argument to DS", file=sys.stderr)
            sys.exit(2)

        data = m.group(2)

        for i in range(len(data)):
            print_char = data[i]

            if print_char == ' ':
                print_char = '[space]'

            code.append(f"{p8(ord(data[i]))} # {print_char}")

        addr += len(data)

    def handle_db(line):
        """
        Handle the DB pseudo-opcode
        """

        nonlocal addr

        m = re.match(REGEX_DB, line, re.IGNORECASE)

        if m is None or m.group(2) is None:
            print(f"line {line}: missing argument to DB", file=sys.stderr)
            sys.exit(2)

        data = m.group(2)

        try:
            val = int(data, 0)

        except ValueError:
            print(f"line {line_num}: invalid integer argument to DB",
                  file=sys.stderr)
            sys.exit(2)

        # Force to byte size
        val &= 0xff

        code.append(f"{p8(val)} # {data}")

        addr += 1

    def check_ops(opcode, op_a, op_b):
        """Check operands for sanity with a particular opcode"""

        def check_ops_count(desired, found):
            # Makes sure we have right operand count
            if found < desired:
                print(f"Line {line_num}: missing operand to {opcode}",
                      file=sys.stderr)
                sys.exit(1)
            elif found > desired:
                print(f"Line {line_num}: unexpected operand to {opcode}",
                      file=sys.stderr)
                sys.exit(1)

        # Make sure we know this opcode at all
        if opcode not in OPCODES:
            print(f"line {line_num}: unknown opcode {opcode}", file=sys.stderr)
            sys.exit(2)

        op_type = OPCODES[opcode]["type"]

        total_operands = 0

        if op_a is not None:
            total_operands += 1

        if op_b is not None:
            total_operands += 1

        if op_type == 0 or op_type == 1 or op_type == 2:
            # 0, 1, or 2 register operands
            check_ops_count(op_type, total_operands)

        elif op_type == 8:
            # LDI r,i or LDI r,label
            check_ops_count(2, total_operands)

    # Type to function mapping
    type_f = {
        0: out0,
        1: out1,
        2: out2,
        8: out8,
    }

    for line in inputfile:
        line_num += 1

        # Strip comments
        comment_index = line.find(';')
        if comment_index != -1:
            line = line[:comment_index]

        # Normalize
        line = line.strip()

        # Ignore blank lines
        if input == '':
            continue

        # print(line)  # debug

        m = re.match(REGEX, line)

        if m is not None:
            label, opcode, op_a, op_b = normalize_line(m.groups())

            # print(label, opcode, op_a, op_b)  # debug

            # Track label address
            if label is not None:
                sym[label] = addr
                # print(f"Label {label}: {addr}")  # debug
                code.append(f'# {label} (address {addr}):')

            if opcode is not None:
                if opcode == 'DS':
                    handle_ds(line)
                elif opcode == 'DB':
                    handle_db(line)
                else:
                    # Check operand count
                    check_ops(opcode, op_a, op_b)

                    # Handle opcodes
                    op_info = OPCODES[opcode]
                    handler = type_f[op_info["type"]]
                    handler(opcode, op_a, op_b, op_info["code"])
        else:
            print(f"No match: {input}", file=sys.stderr)
            sys.exit(3)


def pass2(outputfile, sym, code):
    """
    Output the code, substituting in any symbols.
    """

    for c in code:
        # Replace symbols
        if c[:4] == 'sym:':
            s = c[4:].strip()

            if s in sym:
                c = p8(sym[s])

            else:
                print(f"unknown symbol: {s}", file=sys.stderr)
                sys.exit(2)

        outputfile.write(f"{c}\n")


def main(argv):
    # Parse command line
    inputfile, outputfile = parse_commandline(argv)

    # Open files
    inputfile, outputfile = open_files(inputfile, outputfile)

    # Set up the symbol table
    sym = {}

    # Set up the machine code output
    code = []

    # Assemble
    pass1(inputfile, sym, code)
    pass2(outputfile, sym, code)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
