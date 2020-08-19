"""CPU functionality."""

import sys, os
from pathlib import Path



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*10
        self.ram = [0]*256
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0
        # data_folder = Path("examples/")
        # file_to_open = data_folder / "mult.ls8"
        # For now, we've just hardcoded a program:
        # program = open('examples/' + sys.argv[1])
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]




        if len(sys.argv) != 2:
            print("usage: 02_fileio2.py filename")

        try:
            # print()
            with open('examples/' + sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    x = int(n, 2)
                    print(f"{x:08b}: {x:d}")

                    self.ram[address] = x
                    address += 1

        except:
            print("can not find it!")
            
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
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
        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010
        MUL = 0b10100010
        while self.pc < len(self.ram):
            item = self.ram[self.pc]
            
            if item == PRN:
                print(self.ram_read(self.ram[self.pc+1]))
                self.pc+=1
            elif item == LDI:
                self.ram_write(self.ram[self.pc+1], self.ram[self.pc+2])
                self.pc+=2
            elif item == MUL:
                self.alu('MUL', self.ram[self.pc+1], self.ram[self.pc+2])
                self.pc+=2
            elif item == HLT:
                break

            self.pc += 1


        
