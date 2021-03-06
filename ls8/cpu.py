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
        #stack pointer
        self.reg[7] = 255
        self.opcodes = {
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

    def push(self, mdr):
        self.reg[7] -= 1
        self.ram_write(mdr, self.reg[7])

    def pop(self):
        mdr = self.ram_read(self.reg[7])
        if self.reg[7] < 255:
            self.reg[7] += 1
        return mdr

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def byte(self, value):
        return value & 0xFF

    def get_fl(self, flag):
        if flag == "L":
            return self.fl >> 2
        elif flag == "G":
            return self.fl >> 1 & 0b0000001
        elif flag == "E":
            return self.fl & 0b00000001

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
        elif op == "CMP":
            value_a = self.reg[reg_a]
            value_b = self.reg[reg_b]
            if value_a < value_b:
                self.fl = 0b00000100
            elif value_a > value_b:
                self.fl = 0b00000010
            elif value_a == value_b:
                self.fl = 0b00000001
            else:
                self.fl = 0
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
            is_sub = ir >> 4 & 0b0001

            if operands == 2:
                
                if use_alu:
                    op = ""
                    if ir == self.opcodes["ADD"]:
                        op = "ADD"
                    elif ir == self.opcodes["SUB"]:
                        op = "SUB"
                    elif ir == self.opcodes["MUL"]:
                        op = "MUL"
                    elif ir == self.opcodes["DIV"]:
                        op = "DIV"
                    elif ir == self.opcodes["CMP"]:
                        op = "CMP"
                    else:
                        raise Exception("Unknown opcode. Ending program.")
                    
                    reg_a = self.ram_read(self.pc + 1)
                    reg_b = self.ram_read(self.pc + 2)
                    if self.reg[reg_b] == 0:
                        raise Exception("Error: divide by 0")
                    self.alu(op, reg_a, reg_b)

                elif ir == self.opcodes["LDI"]:
                    reg_a = self.ram_read(self.pc + 1)
                    mdr = self.ram_read(self.pc + 2)
                    self.reg[reg_a] = mdr

            elif operands == 1:
                if ir == self.opcodes["PRN"]:
                    reg_a = self.ram_read(self.pc + 1)
                    print(self.reg[reg_a])
                
                elif ir == self.opcodes["PUSH"]:
                    reg_a = self.ram_read(self.pc + 1)
                    mdr = self.reg[reg_a]
                    self.push(mdr)
                
                elif ir == self.opcodes["POP"]:
                    reg_a = self.ram_read(self.pc + 1)
                    self.reg[reg_a] = self.pop()

                elif ir == self.opcodes["CALL"]:
                    reg_a = self.ram_read(self.pc + 1)
                    mar = self.pc + 2
                    self.push(mar)
                    self.pc = self.reg[reg_a]

                elif ir == self.opcodes["JMP"]:
                    reg_a = self.ram_read(self.pc + 1)
                    print("REG: ", reg_a)
                    print("STACK: ", self.reg[7])
                    print("PC: ", self.pc)
                    self.pc = self.reg[reg_a]

                elif ir == self.opcodes["JEQ"]:
                    if self.get_fl("E") == 1:
                        self.pc = self.reg[self.ram_read(self.pc + 1)]
                    else:
                        is_sub = 0

                elif ir == self.opcodes["JNE"]:
                    if self.get_fl("E") == 0:
                        self.pc = self.reg[self.ram_read(self.pc + 1)]
                    else:
                        is_sub = 0

            elif operands == 0:
                if ir == self.opcodes["HLT"]:
                    halt = True

                elif ir == self.opcodes["RET"]:
                    mar = self.pop()
                    self.pc = mar

                else:
                    raise Exception("Unknown opcode. Ending program.")
            
            if is_sub == 0:
                self.pc += operands + 1 # while