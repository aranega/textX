from textx.metamodel import metamodel_from_str
from pyecore.ecore import *
from textx.export import metamodel_export

from pyecore.resources import ResourceSet

grammar = """
Model:
    'model' name=ID type=Type type=Type
;

Type:
    PrimitiveType|ObjectType
;

PrimitiveType:
    name=INT
;

ObjectType:
    'object' name=ID
;
"""

mm = metamodel_from_str(grammar)
print(mm['Type'].eStructuralFeatures)

# metamodel_export(mm, 'test.dot')

program = mm.model_from_str("""
model test object test 5
""")

print(program.type[0].eContainer())
