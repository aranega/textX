from textx.metamodel import metamodel_from_file
from pyecore.ecore import *

# # Requires a modified version of rhapsody.tx
# meta = metamodel_from_file('rhapsody.tx')
#
# # for x in meta.eAllContents():
# #     print(x)
#
#
# model = meta.model_from_file('LightSwitch.rpy')
#
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
