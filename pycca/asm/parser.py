import re
from . import instructions, register, pointer
from .instruction import Label, Instruction


# Collect all registers in a single namespace for evaluating operands.
_eval_ns = {'st': register.st}
for name in dir(register):
    obj = getattr(register, name)
    if isinstance(obj, register.Register):
        _eval_ns[name] = obj
      
commands = {
    '.byte': lambda *op: bytes(map(int, op)),
    '.p2align': lambda a, b=None, c=None: bytes([int(b, 16)] * int(a)),
    '.asciz': lambda op: bytes(eval(op), 'ascii') + b'\0'
}

def process_command(match):
  cmd, args = match.groups()
  cmd = cmd.strip()
  args = args.strip() if args else None
  
  try:
    result = commands[cmd](*args.split(','))
    #print(f'\tGot assembler command: {cmd}({args.split(",")}) => {result}')
  except KeyError:
    result = b''
    #print(f'[WARN] command "{cmd}" not supported')
  
  return result


def parse_asm(asm, namespace=None):
    """Parse assembly code and return a list of code objects that may be used
    to construct a CodePage.
    
    The *namespace* argument may a dict that defines symbols used in the 
    assembly.
    """
    code = []
    eval_ns = _eval_ns.copy()
    if namespace is not None:
        eval_ns.update(namespace)
        
    # first pass: strip comments and labels
    clean = []
    for i,line in enumerate(asm.split('\n')):
        lineno = i + 1
        line = line.strip()
        origline = line
        if line == '':
            continue
        
        # strip out comments
        line, _, comment = line.partition('#')
        
        # Split line into "label: instr"
        a, part, b = line.partition(':')
        if part == '':
            line = a
        else:
            # create label if needed
            m = re.match(r'\s*([a-zA-Z_][a-zA-Z0-9_]*)', a)
            if m is None:
                raise SyntaxError('Expected label name before ":" on assembly '
                                  'line %d: "%s"' % (lineno, origline))
            label = m.groups()[0]
            clean.append(Label(label))
            line = b
            if label in eval_ns:
                raise NameError('Duplicate symbol "%s" on assembly line %d: "%s"'
                                % (label, lineno, origline))
                
            eval_ns[label] = label
        
        line = line.strip()
        if line == '':
            continue

        clean.append((lineno, line, origline))

    #print(clean)
        
    # second pass: generate instructions
    for line in clean:
        if isinstance(line, Label):
            code.append(line)
            continue
        else:
            lineno, line, origline = line
        
        m = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)([ \t].*)?$', line)
        if m is None:
            # check if it's an instruction for this program (starts with a literal dot)
            m2 = re.match(r'(\.[a-zA-Z_][a-zA-Z0-9_]*)([ \t].*)?$', line)
            
            if m2 is not None:
              data = process_command(m2)
              code.append(data)
              continue
            
            raise SyntaxError('Expected instruction mnemonic or assembler command on assembly line %d:'
                              ' "%s"' % (lineno, origline))
        
        mnem, ops = m.groups()
        mnem = mnem.strip()
        
        # Get instruction class
        try:
            icls = getattr(instructions, mnem)
        except AttributeError:
            raise NameError('Unknown instruction "%s" on assembly line %d:' %
                            (mnem, lineno))
        
        # Use python eval to parse operands
        args = []
        if ops is not None:
            ops = ops.split(',')
            #if mnem == 'lea':
                #print(f'{mnem} {ops}')
            for j, op in enumerate(ops):
                op = op.strip()
                
                # parse pointer size
                m = re.match(r'((byte|word|dword|qword)\s+ptr )?(.*)', op)
                _, ptype, op = m.groups()

                try:
                    ev = eval_ns[op]
                except KeyError:
                    ev = op

                #if mnem == 'lea':
                    #print(f'\t{op} -> {ev, type(ev)}')
                
                # eval operand
                try:
                    arg = eval(op, {'__builtins__': {}}, eval_ns)
                except Exception as err:
                    # this may be an expression of type:
                    # [label + address], which the original code couldn't handle
                    # because at this point, the labels in `eval_ns` merely strings (why tho??)
                    # so, deal with it somehow...
                    #
                    # if this stuff gets parsed as a list, it goes on into instruction.Instruction.__init__
                    # if one of the arguments is a list, it's converted to pointer.Pointer
                    raise type(err)('Error parsing operand "%s" on assembly line'
                                    ' %d:\n    %s' % (op, lineno, str(err)))
                
                # apply pointer size if requested
                if ptype is not None:
                    arg = getattr(pointer, ptype)(arg)
                    
                args.append(arg)

            #if mnem == 'lea':
                #print('\t', icls, args, list(map(type, args)))
        else:
            ops = ''
        
        # Create instruction
        try:
            inst = icls(*args)
            # generate an error here if there is a compile problem:
            inst.code
            code.append(inst)
        except Exception as err:
            raise type(err)('Error creating instruction "%s %s" on assembly line'
                            ' %d:\n    %s' % (mnem, ops, lineno, str(err)))
    
    return code
