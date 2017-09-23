from textx.metamodel import metamodel_from_str
from pyecore.ecore import *

eClass = EPackage('entity_mm')

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

# dynamic EClass
Entity = EClass('Entity')
Entity.eStructuralFeatures.append(EAttribute('name', EString))

Property = EClass('Property')
Property.eStructuralFeatures.append(EAttribute('name', EString))
type_prop = EReference('type', Entity)
Property.eStructuralFeatures.append(type_prop)

Entity.eStructuralFeatures.append(EReference('properties',
                                             Property,
                                             upper=-1,
                                             containment=True))
Entity.eStructuralFeatures.append(EReference('ref_by', Property,
                                             eOpposite=type_prop,  # eopposite works
                                             upper=-1))


# mixed with static EntityEClass
class EntityModel(EObject, metaclass=MetaEClass):
    entities = EReference(eType=Entity, containment=True, upper=-1)

    def __init__(self, *args, **kwargs):
        super().__init__()

# Dynamic EntityModel
# EntityModel = EClass('EntityModel')
# EntityModel.eStructuralFeatures.append(EReference('entities',
#                                                   Entity,
#                                                   containment=True,
#                                                   upper=-1))


# We add the missing eclassifiers
eClass.eClassifiers.extend([Entity, Property])

mm = metamodel_from_str(grammar, classes=eClass.eClassifiers)


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

for o in model.entities:
    if o.ref_by:
        print("I'm {}, my type is {} and I'm referenced by {}"
              .format(o.name, o.eClass, o.ref_by))
