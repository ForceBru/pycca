from .code import Code

def label(name):
    """
    Create a label referencing a location in the code.
    
    The name of this label may be used by other assembler calls that require
    a code pointer. When the label is compiled, it is replaced by its address
    within the CodePage.
    """
    return Label(name)


class Label(object):
    """Marks or references a location in assembly code. 
    """
    def __init__(self, name):
        self.name = name
        
    def __len__(self):
        return 0
        
    def __str__(self):
        return self.name + ':'
        
    def compile(self, symbols):
        return ''

    def __add__(self, disp):
        if not isinstance(disp, int):
            raise TypeError("Can only add integer to label.")
        from .pointer import Pointer
        return Pointer(label=self.name, disp=disp)
        
    def __sub__(self, disp):
        return self + (-disp)
    
    def __radd__(self, x):
        return self + x
        
    def __eq__(self, x):
        return x.name == self.name


class Const:
    def __init__(self):
        self._code = None
        self._len = None
        
    def __len__(self):
        if self._len is None:
            self._len = len(self.code)
        return self._len
        
    @property
    def code(self):
        if self._code is None:
            self._code = self.compile()
        return self._code
        
    def compile(self, symbols=None) -> bytes:
        return b''


class Long(Const):
    """
    `.long` directive.
    
    Usage:
        .long 1, 2, Label_3
        
    Integers are stored as 4-byte numbers, labels are put into `Code` objects.
    """
    def __init__(self, data: list):
        super().__init__()
        
        self.data = [x.strip().replace('.', '_') for x in data]
        
        self._code = None
        self._len = len(data) * 4
        
    def __len__(self):
        return self._len
        
    def __str__(self):
        return '.long ' + ', '.join(self.data)
        
    def compile(self) -> Code:
        unresolved = []
        for entry in self.data:
            try:
                code = int(entry).to_bytes(4, 'little')
            except ValueError:
                code = Code(b'\0' * 4)
                # load absolute address
                code.replace(0, f"{entry}", 'i')
                unresolved.append(code)
            else:
                unresolved.append(Code(code))
                
        self._code = sum(unresolved, Code(b''))
        
        return self._code


class Asciz(Const):
    """
    `.asciz` directive.
    
    Usage:
        .asciz "string", 10, 0
    Integers are converted to bytes, strings are encoded as ASCII.
    """
    def __init__(self, data: list):
        super().__init__()
        self.data = tuple(x.strip() for x in data) + ('0', ) # zero signifies null byte
        self._len = None
        self._code = None
        self._stringified = None
        
    def __len___(self):
        if self._len is None:
            self._len = sum(map(len, self.data))
        return self._len
        
    def __str__(self):
        if self._stringified is None:
            tmp_args = []
            for arg in self.data:
                tmp = ''
                if arg.startswith('"'):  # it's a string
                    for char in arg[1:-1]:  # strip quotes
                        if char.isprintable():
                            tmp += char
                        else:
                            if tmp:
                                tmp_args.append(f'"{tmp}"')
                            tmp_args.append(str(ord(char)))
                            tmp = ''
                    if tmp:
                        tmp_args.append(f'"{tmp}"')
                else:
                    tmp_args.append(arg)
            self._stringified = '.ascii ' + ', '.join(tmp_args)

        return self._stringified
        
    def compile(self) -> bytes:
        ret = b''
        for d in self.data:
            if d[0] == '"': # it's a string
                ret += d[1:-1].encode('ascii')
            else:
                ret += bytes([int(d)])
        return ret
        
    def __eq__(self, x):
        return x.data == self.data
        
        
class Ascii(Asciz):
    def __init__(self, data: list):
        super().__init__(data)
        self.data = self.data[:-1] # strip zero

#class LabelOffset(object):
    #"""References a location in a CodePage that is marked by a label, plus a
    #constant offset.
    #"""
    #def __init__(self, name, offset):
        #self.name = name
        #self.offset = offset
        
    #def __len__(self):
        #return 0
        
    #def __str__(self):
        #return "%s + %d" % (self.name, self.offset)
        
    #def compile(self, symbols):
        #return ''

    #def __add__(self, disp):
        #if not isinstance(disp, int):
            #raise TypeError("Can only add integer to label.")
        #return LabelOffset(self.name, self.offset+disp)
        
    #def __radd__(self, x):
        #return self + x
