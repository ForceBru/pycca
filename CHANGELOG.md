# CHANGELOG
---

### 28.03.2019
1. Fixed bugs in `asm.codepage.CodePage.dump` that showed placeholder bytecode
for label operands even though the labels have already been resolved and the
`CodePage.code` attribute contains correct addresses.
2. Added some assembler commands handling:

       .ascii "String, byte ->", 10, 0
       .asciz "Null-terminated automatically"
       .long 1, 2, 3, 4
    
3. Added ability to use labels as operands, so the following works:

       mov eax, some_label  # moves absolute address
       label:
           .long 1234
           .long other_label
         
4. Added ability to add labels to registers when creating pointers:

       mov eax, dword ptr [ebx + some_label]
       
5. Added ability to define special encoding for instructions with concrete operands,
so that now instructions like `sar r/m8, 1` and `sar r/m8, CL` are supported as well as `sar r/m8, imm8`.
       
5. Added more instructions (some are partially supported):
   1. `div`
   2. `or`
   3. `and`
   4. `sar`
   5. `setcc` (partially)
   6. `cmovcc` (partially)