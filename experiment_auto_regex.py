from textx.metamodel import metamodel_from_str
from pyecore.ecore import *
from textx.export import metamodel_export

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

metamodel_export(mm, 'test.dot')

program = mm.model_from_str("""
widget 44
""")

print(program.name)
