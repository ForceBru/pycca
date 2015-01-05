# -'- coding: utf-8 -'-
from __future__ import division
import sys

from . import ARCH

#   Register definitions
#----------------------------------------

class Register(object):
    """General purpose register.
    """
    def __init__(self, val, name, bits):
        self._val = val
        self._name = name
        self._bits = bits

    @property
    def name(self):
        """Register name
        """
        return self._name

    @property
    def bits(self):
        """Register size in bits
        """
        return self._bits

    @property
    def val(self):
        """3-bit integer code for this register.
        """
        return self._val & 0b111
    
    @property
    def rex(self):
        """Bool indicating value of 4th bit of register code
        """
        return self._val & 0b1000 > 0
        
    def __add__(self, x):
        if isinstance(x, Register):
            return Pointer(reg1=x, reg2=self)
        elif isinstance(x, Pointer):
            return x.__add__(self)
        elif isinstance(x, int):
            return Pointer(reg1=self, disp=x)
        else:
            raise TypeError("Cannot add type %s to Register." % type(x))

    def __radd__(self, x):
        return self + x

    def __sub__(self, x):
        if isinstance(x, int):
            return Pointer(reg1=self, disp=-x)
        else:
            raise TypeError("Cannot subtract type %s from Register." % type(x))

    def __mul__(self, x):
        if isinstance(x, int):
            if x not in [1, 2, 4, 8]:
                raise ValueError("Register can only be multiplied by 1, 2, 4, or 8.")
            return Pointer(reg1=self, scale=x)
        else:
            raise TypeError("Cannot multiply Register by type %s." % type(x))
        
    def __rmul__(self, x):
        return self * x

    def __repr__(self):
        return "Register(0x%x, %s, %d)" % (self._val, self._name, self._bits)
        
    def __str__(self):
        return self._name





# note: see codeproject link for more comprehensive set of x86-64 registers
al = Register(0b000, 'al', 8)  # 8-bit registers (low-byte)
cl = Register(0b001, 'cl', 8)  # r8(/r)
dl = Register(0b010, 'dl', 8)
bl = Register(0b011, 'bl', 8)
ah = Register(0b100, 'ah', 8)  # (high-byte)
ch = Register(0b101, 'ch', 8)
dh = Register(0b110, 'dh', 8)
bh = Register(0b111, 'bh', 8)

ax = Register(0b000, 'ax', 16)  # 16-bit registers
cx = Register(0b001, 'cx', 16)  # r16(/r)
dx = Register(0b010, 'dx', 16)
bx = Register(0b011, 'bx', 16)
sp = Register(0b100, 'sp', 16)
bp = Register(0b101, 'bp', 16)
si = Register(0b110, 'si', 16)
di = Register(0b111, 'di', 16)

eax = Register(0b000, 'eax', 32)  # 32-bit registers   Accumulator (i/o, math, irq, ...)
ecx = Register(0b001, 'ecx', 32)  # r32(/r)            Counter (loop counter and shifts) 
edx = Register(0b010, 'edx', 32)  #                    Data (i/o, math, irq, ...)
ebx = Register(0b011, 'ebx', 32)  #                    Base (base memory addresses)
esp = Register(0b100, 'esp', 32)  #                    Stack pointer
ebp = Register(0b101, 'ebp', 32)  #                    Stack base pointer
esi = Register(0b110, 'esi', 32)  #                    Source index
edi = Register(0b111, 'edi', 32)  #                    Destination index

rax = Register(0b000, 'rax', 64)  # 64-bit registers
rcx = Register(0b001, 'rcx', 64)  # r64(/r)
rdx = Register(0b010, 'rdx', 64)
rbx = Register(0b011, 'rbx', 64)
rsp = Register(0b100, 'rsp', 64)
rbp = Register(0b101, 'rbp', 64)
rsi = Register(0b110, 'rsi', 64)
rdi = Register(0b111, 'rdi', 64)

r8b  = Register(0b1000, 'r8b',  8)  # 64-bit registers, lower byte
r9b  = Register(0b1001, 'r9b',  8)
r10b = Register(0b1010, 'r10b', 8)
r11b = Register(0b1011, 'r11b', 8)
r12b = Register(0b1100, 'r12b', 8)
r13b = Register(0b1101, 'r13b', 8)
r14b = Register(0b1110, 'r14b', 8)
r15b = Register(0b1111, 'r15b', 8)

r8w  = Register(0b1000, 'r8w',  16)  # 64-bit registers, lower word
r9w  = Register(0b1001, 'r9w',  16)
r10w = Register(0b1010, 'r10w', 16)
r11w = Register(0b1011, 'r11w', 16)
r12w = Register(0b1100, 'r12w', 16)
r13w = Register(0b1101, 'r13w', 16)
r14w = Register(0b1110, 'r14w', 16)
r15w = Register(0b1111, 'r15w', 16)

r8d  = Register(0b1000, 'r8d',  32)  # 64-bit registers, lower doubleword
r9d  = Register(0b1001, 'r9d',  32)
r10d = Register(0b1010, 'r10d', 32)
r11d = Register(0b1011, 'r11d', 32)
r12d = Register(0b1100, 'r12d', 32)
r13d = Register(0b1101, 'r13d', 32)
r14d = Register(0b1110, 'r14d', 32)
r15d = Register(0b1111, 'r15d', 32)

r8  = Register(0b1000, 'r8',  64)
r9  = Register(0b1001, 'r9',  64)
r10 = Register(0b1010, 'r10', 64)
r11 = Register(0b1011, 'r11', 64)
r12 = Register(0b1100, 'r12', 64)
r13 = Register(0b1101, 'r13', 64)
r14 = Register(0b1110, 'r14', 64)
r15 = Register(0b1111, 'r15', 64)

mm0 = Register(0b000, 'mm0', 64)  # mm(/r)
mm1 = Register(0b001, 'mm1', 64)
mm2 = Register(0b010, 'mm2', 64)
mm3 = Register(0b011, 'mm3', 64)
mm4 = Register(0b100, 'mm4', 64)
mm5 = Register(0b101, 'mm5', 64)
mm6 = Register(0b110, 'mm6', 64)
mm7 = Register(0b111, 'mm7', 64)

xmm0 = Register(0b000, 'xmm0', 128)  # xmm(/r)
xmm1 = Register(0b001, 'xmm1', 128)
xmm2 = Register(0b010, 'xmm2', 128)
xmm3 = Register(0b011, 'xmm3', 128)
xmm4 = Register(0b100, 'xmm4', 128)
xmm5 = Register(0b101, 'xmm5', 128)
xmm6 = Register(0b110, 'xmm6', 128)
xmm7 = Register(0b111, 'xmm7', 128)


# Lists of registers used as arguments in standard calling conventions
if ARCH == 32:
    # 32-bit stdcall and cdecl push all arguments onto stack
    argi = []
    argf = []
elif ARCH == 64:
    if sys.platform == 'win32':
        argi = [rcx, rdx, r8, r9]
        argf = [xmm0, xmm1, xmm2, xmm3]
    else:
        argi = [rdi, rsi, rdx, rcx, r8, r9]
        argf = [xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7]


from .pointer import Pointer