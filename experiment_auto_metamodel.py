from textx.metamodel import metamodel_from_str
from pyecore.ecore import *

grammar = """
EntityModel:
    entities*=Entity
;

Entity:
    'entity' name=ID '{'
        properties*=Property
    '}'
;

Property:
    name=ID ':' type=[Entity]
;
"""

mm = metamodel_from_str(grammar)
model = mm.model_from_str("""
entity Person {
    name: string
    address: Address
}

entity Address {
    zip: string
}

entity string {
}
""")

for o in model.eAllContents():
    print(o.eClass, o.name, o.eClass)
