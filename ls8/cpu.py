"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0
        self.opcode = {
            "ADD": 0b10100000,
            "AND": 0b10101000,
            "CALL": 0b01010000,
            "CMP": 0b10100111,
            "DEC": 0b01100110,
            "DIV": 0b10100011,
            "HLT": 0b00000001,
            "INC": 0b01100101,
            "INT": 0b01010010,
            "IRET": 0b00010011,
            "JEQ": 0b01010101,
            "JGE": 0b01011010,
            "JGT": 0b01010111,
            "JLE": 0b01011001,
            "JLT": 0b01011000,
            "JMP": 0b01010100,
            "JNE": 0b01010110,
            "LD": 0b10000011,
            "LDI": 0b10000010,
            "MOD": 0b10100100,
            "MUL": 0b10100010,
            "NOP": 0b00000000,
            "NOT": 0b01101001,
            "OR": 0b10101010,
            "POP": 0b01000110,
            "PRA": 0b01001000,
            "PRN": 0b01000111,
            "PUSH": 0b01000101,
            "RET": 0b00010001,
            "SHL": 0b10101100,
            "SHR": 0b10101101,
            "ST": 0b10000100,
            "SUB": 0b10100001,
            "XOR": 0b10101011,
        }

    def load(self, program):
        """Load a program into memory."""
        address = 0
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def byte(self, value):
        return value & 0xFF

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] = self.byte(self.reg[reg_a] + self.reg[reg_b])
        elif op == "SUB":
            self.reg[reg_a] = self.byte(self.reg[reg_a] - self.reg[reg_b])
        elif op == "MUL":
            self.reg[reg_a] = self.byte(self.reg[reg_a] * self.reg[reg_b])
        elif op == "DIV":
            self.reg[reg_a] = self.byte(self.reg[reg_a] // self.reg[reg_b])    
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        halt = False

        while not halt:
            ir = self.ram_read(self.pc)
            operands = ir >> 6
            use_alu = ir >> 5 & 0b001
            if operands == 2:
                if use_alu:
                    op = ""
                    if ir == self.opcode["ADD"]:
                        op = "ADD"
                    elif ir == self.opcode["SUB"]:
                        op = "SUB"
                    elif ir == self.opcode["MUL"]:
                        op = "MUL"
                    elif ir == self.opcode["DIV"]:
                        op = "DIV"
                    else:
                        raise Exception("Unknown opcode. Ending program.")
                    
                    reg_a = self.ram_read(self.pc + 1)
                    reg_b = self.ram_read(self.pc + 2)
                    if self.reg[reg_b] == 0:
                        raise Exception("Error: divide by 0")
                    self.alu(op, reg_a, reg_b)

                elif ir == self.opcode["LDI"]:
                    reg_a = self.ram_read(self.pc + 1)
                    mdr = self.ram_read(self.pc + 2)
                    self.reg[reg_a] = mdr

            elif operands == 1:
                if ir == self.opcode["PRN"]:
                    reg_a = self.ram_read(self.pc + 1)
                    print(self.reg[reg_a])

            elif operands == 0:
                if ir == self.opcode["HLT"]:
                    halt = True

                else:
                    raise Exception("Unknown opcode. Ending program.")

            self.pc += operands + 1 # while