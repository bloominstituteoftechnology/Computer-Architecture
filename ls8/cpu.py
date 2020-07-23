"""CPU functionality."""

import sys
from datetime import datetime
from datetime import timedelta
import threading
import termios
import tty
import os
import time

IM = 5     # interrupt mask (register address)
IS = 6     # interrupt status (register address)
IV = 0xF8  # interrupt vector(s) (ram address)

_fl_l_mask = 0b00000100
_fl_g_mask = 0b00000010
_fl_e_mask = 0b00000001

def cpr(text=''):
    print(text, end='\r\n')

class CPU:
    """Main CPU class."""

    class KeyboardPoller(threading.Thread):
        def __init__(self, callback):
            threading.Thread.__init__(self, daemon=True)
            self.callback = callback
            self._stop_event = threading.Event()
            self.running = False

        def run(self):
            self.running = True
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            while self.running:
                key = None
                try:
                    tty.setcbreak(fd)
                    key = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSAFLUSH, old_settings)
                if key is not None:
                    self.callback(key)

        def stop(self):
            self._stop_event.set()
            self.running = False

        def stopped(self):
            return self._stop_event.is_set() and self.running == False


    ops = {
        0x52: "INT",   # interrupt
    }

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 7
        self.reg.append(0xF4)
        self.pc = 0  # program counter (address of executing instruction)
        self.fl = 0  # flags
        self._dispatch = {
            0x00: self._nop,
            0x01: self._hlt,
            0x47: self._prn,
            0x48: self._pra,
            0x82: self._ldi,  # load integer
            0x50: self._call,
            0x54: self._jmp,
            0x55: self._jeq,
            0x56: self._jne,
            0x57: self._jgt,
            0x58: self._jlt,
            0x59: self._jle,
            0x5A: self._jge,
            0x11: self._ret,
            0x13: self._iret,
            0x45: self._push,
            0x46: self._pop,
            0x83: self._ld,
            0x84: self._st,
        }
        self._alu_dispatch = {
            0xA0: self._add,
            0xA1: self._sub,
            0xA2: self._mul,
            0xA3: self._div,
            0xA4: self._mod,
            0x65: self._inc,
            0x66: self._dec,
            0xA7: self._cmp,
            0xA8: self._and,
            0x69: self._not,
            0xAA: self._or,
            0xAB: self._xor,
            0xAC: self._shl,
            0xAD: self._shr
        }
        self.keyboard_poller = CPU.KeyboardPoller(self.__handle_keypress)
        self.sp = 0xF4  # stack pointer
        self.running = False
        self._can_interrupt = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) < 2:
            cpr("ERROR: no filename argument")
            return

        address = 0

        with open(sys.argv[1], 'r') as program_file:
            for line in program_file:
                comment_index = line.find('#')
                if comment_index != -1:
                    line = line[:comment_index]
                line = line.strip()
                if len(line) == 0:
                    continue
                self.ram[address] = int(line, 2)
                address += 1

    def alu(self, ir, reg_a, reg_b):
        """ALU operations."""

        operation = self._alu_dispatch.get(ir)
        arg_count = self._arg_count(ir)

        if operation is None:
            raise Exception("Unsupported ALU operation")
        elif arg_count == 1:
            operation(reg_a)
        elif arg_count == 2:
            operation(reg_a, reg_b)

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        cpr()

    def _arg_count(self, ir):
        return ir >> 6

    def run(self):
        """Run the CPU."""
        self.running = True
        last_runloop = datetime.now()
        interrupt_interval = timedelta(seconds=0)
        self.keyboard_poller.start()

        while self.running:
            # self.trace()
            self._jumped = False
           
            # interrupt timer update
            now = datetime.now()
            interrupt_interval += (now - last_runloop)
            last_runloop = now
            if interrupt_interval.seconds >= 1:
                self.reg[IS] |= 0b00000001
                interrupt_interval -= timedelta(seconds=1)

            # prepare instruction
            ir = self.ram_read(self.pc)  # instruction register

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            args = self._arg_count(ir)

            # perform instruction
            if ir & 0b00100000:
                self.alu(ir, operand_a, operand_b)
            else:
                operation = self._dispatch.get(ir)

                if operation is None:
                    raise Exception("Unsupported operation")
                elif args == 1:
                    operation(operand_a)
                elif args == 2:
                    operation(operand_a, operand_b)
                else:
                    operation()

            # set program counter (if necessary)
            if not self._jumped:
                self.pc += args + 1

            # handle interrupt
            if self._can_interrupt:
                self.__handle_interrupts()

    def __handle_interrupts(self):
        masked_interrupts = self.reg[IM] & self.reg[IS]
        for i in range(8):
            mask = (1 << i)
            if masked_interrupts & mask:
                masked_interrupts &= ~mask
                self.reg[IS] &= ~mask
                self._can_interrupt = False
                (temp0, temp1) = (self.reg[0], self.reg[1])
                (self.reg[0], self.reg[1]) = (self.pc, self.fl)
                self._push(0)
                self._push(1)
                (self.reg[0], self.reg[1]) = (temp0, temp1)
                for r in range(7):
                    self._push(r)
                self.pc = self.ram[IV + i]
                return

    def __handle_keypress(self, key):
        num = ord(key)
        if num == 27 or num == 4:  # esc or ctrl-D; exit
            self._hlt()
        self.ram[0xF4] = ord(key)
        self.reg[IS] |= 0b00000010

    def _nop(self):
        pass

    def _hlt(self):
        self.keyboard_poller.stop()
        self.running = False

    def _ldi(self, reg_address, value):
        self.reg[reg_address] = value

    def _prn(self, reg_address):
        cpr(self.reg[reg_address])

    def _pra(self, reg_adr):
        item = self.reg[reg_adr]
        if isinstance(item, int):
            print(chr(item), end='')
        else:
            print(item, end='')

    def _add(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]

    def _sub(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] - self.reg[reg_b]

    def _mul(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

    def _div(self, reg_a, reg_b):
        operand_b = self.reg[reg_b]
        if operand_b == 0:
            cpr("Error: Cannot divide by zero")
            self._hlt()
            return
        self.reg[reg_a] = self.reg[reg_a] / operand_b

    def _mod(self, reg_a, reg_b):
        operand_b = self.reg[reg_b]
        if operand_b == 0:
            cpr("Error: Cannot divide by zero")
            self._hlt()
            return
        self.reg[reg_a] = self.reg[reg_a] % operand_b

    def _inc(self, op):
        self.reg[op] += 1

    def _dec(self, op):
        self.reg[op] -= 1

    def _cmp(self, op1, op2):
        (a, b) = (self.reg[op1], self.reg[op2])
        if a == b:
            self.fl = _fl_e_mask
        elif a < b:
            self.fl = _fl_l_mask
        elif a > b:
            self.fl = _fl_g_mask

    def _and(self, op1, op2):
        self.reg[op1] = self.reg[op1] & self.reg[op2]

    def _not(self, op1):
        self.reg[op1] = ~self.reg[op1]

    def _or(self, op1, op2):
        self.reg[op1] = self.reg[op1] | self.reg[op2]

    def _xor(self, op1, op2):
        self.reg[op1] = self.reg[op1] ^ self.reg[op2]

    def _shl(self, op1, op2):
        self.reg[op1] = self.reg[op1] << self.reg[op2]

    def _shr(self, op1, op2):
        self.reg[op1] = self.reg[op1] >> self.reg[op2]

    def _push(self, adr):
        self.sp -= 1
        self.ram[self.sp] = self.reg[adr]

    def _pop(self, adr):
        self.reg[adr] = self.ram[self.sp]
        self.sp += 1

    def _call(self, adr):
        reg0 = self.reg[0]  # temp value for register
        # push next instruction to stack
        self.reg[0] = self.pc + 2
        self._push(0)
        self.reg[0] = reg0  # put old reg value back in register
        # jump to call site
        self.pc = self.reg[adr]
        self._jumped = True

    def _ret(self):
        reg0 = self.reg[0]
        self._pop(0)
        self.pc = self.reg[0]
        self.reg[0] = reg0
        self._jumped = True

    def _st(self, reg_a, reg_b):
        self.ram[self.reg[reg_a]] = self.reg[reg_b]

    def _ld(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram[self.reg[reg_b]]

    def _jmp(self, reg_adr):
        self.pc = self.reg[reg_adr]
        self._jumped = True

    def _jeq(self, adr):
        if self.__fl_equal():
            self._jmp(adr)
            self._jumped = True

    def _jne(self, adr):
        if not self.__fl_equal():
            self._jmp(adr)
            self._jumped = True

    def _jlt(self, adr):
        if self.__fl_less():
            self._jmp(adr)
            self._jumped = True

    def _jgt(self, adr):
        if self.__fl_greater():
            self._jmp(adr)
            self._jumped = True

    def _jle(self, adr):
        if self.__fl_less() or self.__fl_equal():
            self._jmp(adr)
            self._jumped = True

    def _jge(self, adr):
        if self.__fl_greater() or self.__fl_equal():
            self._jmp(adr)
            self._jumped = True

    def _iret(self):
        for r in range(6, -1, -1):
            self._pop(r)
        (temp0, temp1) = (self.reg[0], self.reg[1])
        self._pop(0)
        self._pop(1)
        (self.fl, self.pc) = (self.reg[0], self.reg[1])
        (self.reg[0], self.reg[1]) = (temp0, temp1)

        self._can_interrupt = True
        self._jumped = True

    def __fl_equal(self):
        return self.fl & _fl_e_mask == _fl_e_mask

    def __fl_less(self):
        return self.fl & _fl_l_mask == _fl_l_mask

    def __fl_greater(self):
        return self.fl & _fl_g_mask == _fl_g_mask
