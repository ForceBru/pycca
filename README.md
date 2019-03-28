PyCCA: Pure-python assembler
===========================================

Luke Campagnola, 2014

ForceBru, 2018


> Documentation: http://pycca.readthedocs.org/en/latest/<br>
> Source: http://github.com/pycca/pycca<br>
> Installation: `pip install pycca`


Motivation
----------

Python is an excellent platform for numerical computing but relies
heavily on compiled modules to provide optimized functions. For 
distributed packages, this either increases the burden on the developer
to produce compiled binaries for a variety of platforms, or increases
the burden on the end user to compile the package or its binary 
dependencies. Consequently, many Python developers avoid optimzed
code, preferring instead to advertise "pure-python" as a feature
of their packages.

The objective of pycca is to provide a pure-python approach that
allows assembly to be assembled to bytecode and/or relocatable libraries of sorts
with no external dependencies. 


Approach
--------

This version does _not_ execute the assembled bytecode (although it should be
fairly trivial to add back). The goal is to have a real-life x86 assembler written
in plain Python, and thus executable everywhere Pythons runs.


Status
------

|  **Assembler:**   | **beta**                        |
|-------------------|---------------------------------|
|  C compiler:      |   **probably isn't happening**  |


* Functional assembly compiler with a relatively limited set of instructions
  (see `examples.py` and `pycca/asm/instructions.py`). All instructions
  are tested to produce identical output to the GNU assembly compiler.
* Assembly examples have been tested on:

  |           |            |  Linux  |   OSX   | Windows |
  |:----------|:-----------|:-------:|:-------:|:-------:|
  |  IA-32    | Python 2.7 |    X    |         |    X    |
  |           | Python 3.4 |    X    |         |         |
  | Intel-64  | Python 2.7 |    X    |    X    |         |
  |           | Python 3.4 |    X    |         |    X    |

* Unit tests pass on 64-bit and 32-bit Linux under python 2.7 and 3.4

