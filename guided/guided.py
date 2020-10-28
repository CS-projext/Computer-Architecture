import sys

# Memory
# Array of bytes, use index to specify address
# "opcode" == the instruction byte
# "operands" == arguments to the instruction
PRINT_NAME = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4

memory = [
  1, # PRINT
  3, # SAVE_REG R1, 37
  1,
  37,
  4, # PRINT_REG
  1, # PRINT_REG R1
  1, # PRINT
  2, # HALT
]

# Variables are called "registers", R0 - R7
# Registers can hold a single byte

register = [0] * 8

# Start execution at address 0
# Keep track of the address of the currently-executing instruction
pc = 0  # Program counter, pointer to the instruction

halted = False

while not halted:
    instruction = memory[pc]

    if instruction == 1:
        print("Drew")

    elif instruction == 2:
        halted = True
    
    elif instruction == 3: # SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 2
        
    elif instruction == 4: # PRINT_REG
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 1

    else:
        print(f"unknown instruction {instruction}")

    pc += 1