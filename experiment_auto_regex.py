from textx.metamodel import metamodel_from_str
from pyecore.ecore import *

grammar = """
Move:
  'widget' name=AB
;

A:
    'state' name=ID
;

AB:
    INT|/(\w|\+|-)+/
;



"""

mm = metamodel_from_str(grammar)

print()

program = mm.model_from_str("""
widget 44
""")

print(program.name)
