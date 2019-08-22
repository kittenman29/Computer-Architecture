"""CPU functionality."""

import sys


# stack pointer
sp = 7

HLT  = 0b00000001
LDI  = 0b10000010
PRN  = 0b01000111
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
ADD  = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0  # program counter
        self.halted = False
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[sp] = 0xF4

    def ram_write(self, address, value):
        self.ram[address] = value
    
    def ram_read(self, address):
        return self.ram[address]

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    # Split before and after any comment symbols
                    comment_split = line.split("#")

                    num = comment_split[0].strip()
                    # print("num", num)

                    # Ignore blanks
                    if num == "":
                        continue

                    value = int(num, 2)
                    # print("value", value)
                    # print("self.ram[address]", self.ram[address])

                    self.ram[address] = value
                    
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
    
        running = True
        while running:
            # print("something", self.ram[self.pc])
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1) # read the next line in the machine code
            operand_b = self.ram_read(self.pc + 2) # second next line in the machine code

            if ir == HLT:
                running = False
                sys.exit(1)

            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            
            elif ir == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            elif ir == PUSH:
                self.reg[sp] -= 1 #setting stack pointer down one index in memory
                self.ram_write(self.reg[sp], self.reg[operand_a])
                self.pc += 2
            
            elif ir == POP:
                self.reg[operand_a] = self.ram_read(self.reg[sp])
                self.reg[sp] += 1
                self.pc += 2

            elif ir == CALL:
                
                self.reg[sp] -= 1
                self.ram_write(self.reg[sp], self.pc + 2)

                
                self.pc = self.reg[operand_a]
            
            elif ir == RET:
                self.pc = self.ram_read(self.reg[sp])
                self.reg[sp] += 1
            
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            
            else:
                print(f"Unknown instruction: {ir}")
                break

