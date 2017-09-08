from textx.metamodel import metamodel_from_str
from pyecore.ecore import *

grammar = """
RhapsodyModel:
    header= /[^\n]*/
    root=Object
;

Object:
    '{' name=ID
        properties+=Property
    '}'
;

Property:
    '-' name=ID '=' (values=Value (';'? !('-'|'}') values=Value)*)? ';'?
;

Value:
     STRING | INT | FLOAT | GUID | Object | ID
;

GUID:
    'GUID' value=/[a-f0-9]*-[a-f0-9]*-[a-f0-9]*-[a-f0-9]*-[a-f0-9]*/
;
"""

mm = metamodel_from_str(grammar)

model = mm.model_from_str("""
I-Logix-RPY-Archive version 8.7.1 C++ 5066837
{ IProject
	- _id = GUID b335390e-08e9-4022-8204-5eefee0b3d18;
}
""")

for o in model.eAllContents():
    print(o.eClass, [x.name for x in o.eClass.eStructuralFeatures])
