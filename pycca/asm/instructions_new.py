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
