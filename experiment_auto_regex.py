from textx.metamodel import metamodel_from_str
from pyecore.ecore import *

grammar = """
Modifier:
    (static?='static' final?='final' visibility=Visibility)#
;

Visibility:
    'public' | 'private' | 'protected';
"""

mm = metamodel_from_str(grammar)

program = mm.model_from_str("""
final private
""")

print(program.static)
