from collections import OrderedDict
from .instruction import Instruction


class neg(Instruction):
  name = 'neg'
  
  modes = {
    ('r/m8', ): ['f6 /3', 'M', True, True],
    ('r/m16',): ['f7 /3', 'M', True, True],
    ('r/m32',): ['f7 /3', 'M', True, True],
  }
  
  operand_enc = {
    'M': ['ModRM:r/m (r,w)']
  }
  
  
class div(Instruction):
    name = 'div'
    
    modes = {
        ('r/m8', ): ['F6 /6', 'M', 1,1],
        ('r/m16', ): ['F7 /6', 'M', 1,1],
        ('r/m32', ): ['F7 /6', 'M', 1,1],
    }
    
    operand_enc = {
        'M': ['ModRM:r/m (w)']
    }
    

class xor(Instruction):
  name = 'xor'

  modes = {
    #('al', 'imm8'): ['34', 'I', 1, 1],
    #('ax', 'imm16'): ['35', 'I', 1, 1],
    #('eax', 'imm32'): ['35', 'I', 1, 1],

    ('r/m8', 'imm8'): ['80 /6', 'MI', 1, 1],
    ('r/m16', 'imm16'): ['81 /6', 'MI', 1, 1],
    ('r/m32', 'imm32'): ['81 /6', 'MI', 1, 1],

    ('r/m16', 'imm8'): ['83 /6', 'MI', 1, 1],
    ('r/m16', 'imm16'): ['83 /6', 'MI', 1, 1],

    ('r/m8', 'r8'): ['30 /r', 'MR', 1, 1],
    ('r/m16', 'r16'): ['31 /r', 'MR', 1, 1],
    ('r/m32', 'r32'): ['31 /r', 'MR', 1, 1],

    ('r8', 'r/m8'): ['32 /r', 'RM', 1, 1],
    ('r16', 'r/m16'): ['33 /r', 'RM', 1, 1],
    ('r32', 'r/m32'): ['33 /r', 'RM', 1, 1],
    }

  operand_enc = {
    #'I' : ['al/ax/eax', 'imm8/16/32'],
    'MI': ['ModRM:r/m (r,w)', 'imm8/16/32'],
    'MR': ['ModRM:r/m (r,w)', 'ModRM:reg (r)'],
    'RM': ['ModRM:reg (r,w)', 'ModRM:r/m (r)']
    }
    

class or_(Instruction):
  name = 'or'

  modes = {
    #('al', 'imm8'): ['34', 'I', 1, 1],
    #('ax', 'imm16'): ['35', 'I', 1, 1],
    #('eax', 'imm32'): ['35', 'I', 1, 1],

    ('r/m8', 'imm8'): ['80 /1', 'MI', 1, 1],
    ('r/m16', 'imm16'): ['81 /1', 'MI', 1, 1],
    ('r/m32', 'imm32'): ['81 /1', 'MI', 1, 1],

    ('r/m16', 'imm8'): ['83 /1', 'MI', 1, 1],
    ('r/m32', 'imm8'): ['83 /1', 'MI', 1, 1],

    ('r/m8', 'r8'): ['08 /r', 'MR', 1, 1],
    ('r/m16', 'r16'): ['09 /r', 'MR', 1, 1],
    ('r/m32', 'r32'): ['09 /r', 'MR', 1, 1],

    ('r8', 'r/m8'): ['0A /r', 'RM', 1, 1],
    ('r16', 'r/m16'): ['0B /r', 'RM', 1, 1],
    ('r32', 'r/m32'): ['0B /r', 'RM', 1, 1],
    }

  operand_enc = {
    #'I' : ['al/ax/eax', 'imm8/16/32'],
    'MI': ['ModRM:r/m (r,w)', 'imm8/16/32'],
    'MR': ['ModRM:r/m (r,w)', 'ModRM:reg (r)'],
    'RM': ['ModRM:reg (r,w)', 'ModRM:r/m (r)']
    }
    
    
class and_(Instruction):
  name = 'and'

  modes = {
    #('al', 'imm8'): ['34', 'I', 1, 1],
    #('ax', 'imm16'): ['35', 'I', 1, 1],
    #('eax', 'imm32'): ['35', 'I', 1, 1],

    ('r/m8', 'imm8'): ['80 /4', 'MI', 1, 1],
    ('r/m16', 'imm16'): ['81 /4', 'MI', 1, 1],
    ('r/m32', 'imm32'): ['81 /4', 'MI', 1, 1],

    ('r/m16', 'imm8'): ['83 /4', 'MI', 1, 1],
    ('r/m32', 'imm8'): ['83 /4', 'MI', 1, 1],

    ('r/m8', 'r8'): ['20 /r', 'MR', 1, 1],
    ('r/m16', 'r16'): ['21 /r', 'MR', 1, 1],
    ('r/m32', 'r32'): ['21 /r', 'MR', 1, 1],

    ('r8', 'r/m8'): ['22 /r', 'RM', 1, 1],
    ('r16', 'r/m16'): ['23 /r', 'RM', 1, 1],
    ('r32', 'r/m32'): ['23 /r', 'RM', 1, 1],
    }

  operand_enc = {
    #'I' : ['al/ax/eax', 'imm8/16/32'],
    'MI': ['ModRM:r/m (r,w)', 'imm8/16/32'],
    'MR': ['ModRM:r/m (r,w)', 'ModRM:reg (r)'],
    'RM': ['ModRM:reg (r,w)', 'ModRM:r/m (r)']
    }
    
    
class sar(Instruction):
    name = 'sar'
    
    modes = {
        ('r/m8', '1'): ['D0 /7', 'M1', True, True],
        ('r/m8', 'CL'): ['D2 /7', 'MC', True, True],
        ('r/m8', 'imm8'): ['C0 /7', 'MI', True, True],
        
        ('r/m16', '1'): ['D1 /7', 'M1', True, True],
        ('r/m16', 'CL'): ['D3 /7', 'MC', True, True],
        ('r/m16', 'imm8'): ['C1 /7', 'MI', True, True],
        
        ('r/m32', '1'): ['D1 /7', 'M1', True, True],
        ('r/m32', 'CL'): ['D3 /7', 'MC', True, True],
        ('r/m32', 'imm8'): ['C1 /7', 'MI', True, True],
    }
    
    operand_enc = {
        'M1': ['ModRM:r/m (r,w)', '1'],
        'MC': ['ModRM:r/m (r,w)', 'CL'],
        'MI': ['ModRM:r/m (r,w)', 'imm8'],
    }
    
    
class adc(Instruction):
    name = 'adc'
    
    modes = {
        ('AL', 'imm8'): ['14', 'I', 1, 1],
        ('AX', 'imm16'): ['15', 'I', 1, 1],
        ('EAX', 'imm32'): ['15', 'I', 1, 1],
        
        ('r/m8', 'imm8'): ['80 /2', 'MI', 1, 1],
        ('r/m16', 'imm16'): ['81 /2', 'MI', 1, 1],
        ('r/m32', 'imm32'): ['81 /2', 'MI', 1, 1],
        
        ('r/m8', 'r8'): ['10 /r', 'MR', 1, 1],
        ('r/m16', 'r16'): ['11 /r', 'MR', 1, 1],
        ('r/m32', 'r32'): ['11 /r', 'MR', 1, 1],
        
        ('r8', 'r/m8'): ['12 /r', 'RM', 1, 1],
        ('r16', 'r/m16'): ['13 /r', 'RM', 1, 1],
        ('r32', 'r/m32'): ['13 /r', 'RM', 1, 1],
    }
    
    operand_enc = {
        'RM': ['ModRM:reg (r,w)', 'ModRM:r/m (r)'],
        'MR': ['ModRM:r/m (r,w)', 'ModRM:reg (r)'],
        'MI': ['ModRM:r/m (r,w)', 'imm8/16/32'],
        'I': ['AL/AX/EAX', 'imm8/16/32']  # TODO: does this work?
    }


class movsx(Instruction):
  name = 'movsx'
  
  modes = {
    ('r16', 'r/m8'): ['0fbe /r', 'RM', True, True],
    ('r32', 'r/m8'): ['0fbe /r', 'RM', True, True],
    ('r32', 'r/m16'): ['0fbf /r', 'RM', True, True],
  }
  
  operand_enc = {
    'RM': ['ModRM:reg (w)', 'ModRM:r/m (r)']
  }
  
class movsxd(movsx):
  name = 'movsxd'
  
  modes = {
    ('r16', 'r/m16'): ['63 /r', 'RM', True, True],
    ('r32', 'r/m32'): ['63 /r', 'RM', True, True],
  }
  
class movzx(movsx):
  name = 'movzx'
  
  modes = {
    ('r16', 'r/m8'): ['0fb6 /r', 'RM', True, True],
    ('r32', 'r/m8'): ['0fb6 /r', 'RM', True, True],
    ('r32', 'r/m16'): ['0fb7 /r', 'RM', True, True],
  }
  
 
def _setcc(name, opcode, doc):
    """Create a setcc instruction class.
    """
      
    modes = {
        # the '/0' is arbitrary because these instructions do not care about the 'reg' field of the ModRM byte
        ('r/m8',): [opcode + ' /0', 'M', True, True],
    }

    op_enc = {
        'M': ['ModRM:r/m (r)'],
    }

    d = " Accepts an 8-bit register or memory location."
    return type(name, (Instruction, ), {
        'modes': modes,
        'operand_enc': op_enc,
        '__doc__': doc + d,
        
        })


setne = _setcc('setne', '0f95', 'Set byte if not equal (ZF=0)')
setle = _setcc('setle', '0f9e', 'Set byte if not equal (ZF=0)')


def _cmovcc(name, opcode, doc):
    """Create a cmovcc instruction class.
    """
      
    modes = {
        ('r16', 'r/m16'): [opcode, 'RM', True, True],
        ('r32', 'r/m32'): [opcode, 'RM', True, True],
    }

    op_enc = {
        'RM': ['ModRM:reg (r, w)', 'ModRM:r/m (r)'],
    }

    d = " Accepts an 8-bit register or memory location."
    return type(name, (Instruction, ), {
        'modes': modes,
        'operand_enc': op_enc,
        '__doc__': doc + d,
        
        })
        
cmovne = _cmovcc('cmovne', '0f45 /r', 'Move if not equal (ZF=0)')
    
class cdq(Instruction):
  name = 'cdq'
  
  modes = OrderedDict([
    ((), ['99', None, True, True])
    ])
    
  operand_enc = {}
  
class cbw(Instruction):
  name = 'cbw'
  
  modes = OrderedDict([
    ((), ['98', None, True, True])
    ])
    
  operand_enc = {}
  
class cwde(cbw):
  name = 'cwde'
