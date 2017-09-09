from textx.metamodel import metamodel_from_file, metamodel_from_str
from pyecore.ecore import *

# Requires a modified version of rhapsody.tx
meta = metamodel_from_file('a.tx')

for x in meta.eAllContents():
    if isinstance(x, EReference):
        print(x.eType.eStructuralFeatures[0].eType.ePackage.nsURI)


program = """model test_model {
    kind zoub
    kind toto
    kind zeft
    kind fjsj
}
"""

model = meta.model_from_str(program)

print([x.name for x in model.kinds])

#
# def num_parent(o, i=0):
#     if o.eContainer() is None:
#         return i
#     else:
#         return 1 + num_parent(o.eContainer())
#
#
# a = list(model.eAllContents())
# a.sort(key=lambda x: num_parent(x))
# print(a[-1], num_parent(a[-1]))
#
# e = a[-1]
# while e.eContainer() is not None:
#     if hasattr(e, 'value'):
#         print(e.value)
#     else:
#         print(e.name)
#     e = e.eContainer()
