# -'- coding: utf-8 -'-

import sys, mmap, ctypes
from .instruction import Instruction, Code, Label
from .parser import parse_asm

from .label import Const


class CodePage(object):
    """Compiles assembly, loads machine code into executable memory, and 
    generates python functions for accessing the code.
    
    Initialize with either an assembly string or a list of 
    :class:`Instruction <pycc.asm.Instruction>` instances. The *namespace*
    argument may be used to define extra symbols when compiling from an 
    assembly string. 
    
    This class encapsulates a block of executable mapped memory to which a 
    sequence of asm commands are compiled and written. The memory page(s) may 
    contain multiple functions; use get_function(label) to create functions 
    beginning at a specific location in the code.
    """
    def __init__(self, asm, namespace=None):
        self.labels = {}
        if isinstance(asm, str):
            asm = parse_asm(asm, namespace=namespace)
        else:
            if namespace is not None:
                raise TypeError("Namespace argument may only be used with "
                                "string assembly type.")
        
        self.asm = asm
        self.page_addr = 0
        
        # Compile machine code and write to the page.
        self.code = self.compile(asm)
        self._length = None
        
    def __len__(self):
        return sum(map(len, self.asm))

    def compile(self, asm):
        ptr = self.page_addr
        # First locate all labels
        for cmd in asm:
            ptr += len(cmd)
            if isinstance(cmd, Label):
                self.labels[cmd.name] = ptr
                
        # now compile
        symbols = self.labels.copy()
        code = b''
        for cmd in asm:
            if isinstance(cmd, Label):
                continue
            
            if isinstance(cmd, (Instruction, Const)):
                # if there are unresolved symbols
                if isinstance(cmd.code, Code):
                    # Make some special symbols available when resolving
                    # expressions:
                    symbols['instr_addr'] = self.page_addr + len(code)
                    symbols['next_instr_addr'] = symbols['instr_addr'] + len(cmd)
                    
                    # actually resolve `cmd.code`
                    cmd._code = cmd.code.compile(symbols)
                    
                assert isinstance(cmd.code, bytes)
                cmd = cmd.code
            code += cmd
        # TODO: could just return a `Code` instance, which'll hopefully make the code relocatable
        return code

    def dump(self):
        """Return a string representation of the machine code and assembly
        instructions contained in the code page.
        """
        code = ''
        ptr = 0
        indent = ''
        for instr in self.asm:
            hex = ''
            
            if isinstance(instr, Instruction):
                hex = ''.join(f'{b:02x}' for b in instr.code)
            elif isinstance(instr, Const): # just raw data
                if not instr.code:
                    continue
                hex = ''.join(f'{b:02x}' for b in instr.code)
              
            pad = ' ' * (40 - len(hex))
            
            if isinstance(instr, Label):
                if indent:
                    indent = ''
              
            code += f'0x{ptr:04x}: {hex}{pad}{indent}{instr}\n'

            if isinstance(instr, Label):
                indent = ' ' * 2
            
            ptr += len(hex)//2
        return code

