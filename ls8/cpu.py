"""CPU functionality."""

import sys, os
from pathlib import Path

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
DIV = 0b10100011
ADD = 0b10100000 
SUB = 0b10100001 
CALL = 0b01010000 
RET = 0b00010001
PUSH = 0b01000101 
POP = 0b01000110 
CMP = 0b10100111 
JMP = 0b01010100 
JEQ = 0b01010101 
JNE = 0b01010110 
AND = 0b10101000 
OR = 0b10101010 
XOR = 0b10101011 
NOT = 0b01101001  
SHL = 0b10101100 
SHR = 0b10101101  
MOD = 0b10100100 

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*10
        self.ram = [0]*256
        self.pc = 0
        self.halted = False

    def load(self, filename):
        """Load a program into memory."""



        try:
            address = 0

            with open('examples/' + filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    x = int(n, 2)
                    # print(f"{x:08b}: {x:d}")

                    self.ram[address] = x
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found!")
            sys.exit(2)

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    def push(self, op_a):
        reg_index = op_a
        value = self.reg[reg_index]
        self.reg[7] -= 1
        self.ram[self.reg[7]] = value

    def pop(self, op_a):
        reg_index = op_a
        value = self.ram[self.reg[7]]
        self.reg[reg_index] = value
        self.reg[7] += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == "MOD":
            pass
        elif op == "OR":
            pass
        elif op == "XOR":
            pass
        elif op == "NOT":
            pass
        elif op == "SHR":
            pass
        elif op == "SHL":
            pass
        elif op == "AND":
            pass
        else:
            raise Exception("Unsupported ALU operation")

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

        print()

    




    def run(self):
        """Run the CPU."""
        while not self.halted:
            # print(self.ram_read(self.pc))
            cmd = self.ram[self.pc]
            cmd_len = ((cmd >> 6) & 0b11) + 1
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            
            if cmd == PRN:
                print(self.reg[op_a])
            
            elif cmd == PUSH:
                self.push(op_a)
            
            elif cmd == POP:
                self.pop(op_a)
     
            elif cmd == LDI:
                self.reg[op_a] = op_b
        
            elif cmd == MUL:
                self.alu('MUL', op_a, op_b)

            elif cmd == HLT:
                self.halted = True

            self.pc += cmd_len


        
