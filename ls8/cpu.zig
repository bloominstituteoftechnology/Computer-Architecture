const std = @import("std");

const PROGRAM = [_]u8{
    // From print8.ls8
    0b10000010, // LDI R0,8
    0b00000000,
    0b00001000,
    0b01000111, // PRN R0
    0b00000000,
    0b00000001, // HLT
};

pub fn main() !void {
    std.log.info(.LS8_CpuMain, "Hello, world!", .{});

    var cpu = Cpu.init();

    std.mem.copy(u8, &cpu.ram, &PROGRAM);
}

pub const Cpu = struct {
    ram: [256]u8,
    registers: [8]u8,

    /// Address of the currently executing instruction
    program_counter: u8,

    /// Contains a copy of the currently executing instruction
    instruction_register: u8,

    /// The memory address we're reading or writing
    memory_address_register: u8,

    /// The data to write or the value just read from memory
    memory_data_register: u8,

    /// How two numbers compared to each other
    flags: packed struct {
        less_than: bool,
        greater_than: bool,
        equal: bool,
    },

    /// Which register holds the Interrupt Mask
    pub const IM = 5;

    /// Which register holds the Interrupt Status
    pub const IS = 6;

    /// Which register holds the Stack Pointer
    pub const SP = 7;

    /// The initial value of the stack register
    pub const MEM_ADDR_KEY_PRESSED = 0xF4;

    /// The initial value of the stack register
    pub const STACK_INIT = 0xF3;

    pub fn init() @This() {
        var registers = [_]u8{0} ** 8;
        registers[SP] = STACK_INIT;

        return .{
            // Initialize ram to 0
            .ram = [_]u8{0} ** 256,
            .registers = registers,
            .program_counter = 0,
            .instruction_register = 0,
            .memory_address_register = 0,
            .memory_data_register = 0,
            .flags = .{
                .less_than = false,
                .greater_than = false,
                .equal = false,
            },
        };
    }
};
