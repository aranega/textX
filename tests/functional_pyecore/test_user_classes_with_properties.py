import pytest  # noqa
from textx.metamodel import metamodel_from_str
from pyecore.ecore import EMetaclass, EInt, EAttribute

grammar = """
    UserModel:
        a = INT
    ;
"""


@EMetaclass
class UserModel(object):
    _a = EAttribute('a', eType=EInt, derived=True)

    def __init__(self, a):
        self._a = a

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, new_val):
        self._a = new_val


def test_user_classes_with_properties():
    """
    Test that user class may have property that is
    called the same as one of attributes defined in
    meta-model.
    """

    test_mm = metamodel_from_str(grammar, classes=[UserModel])
    model = test_mm.model_from_str("42")

    assert model
    assert type(model) is UserModel
    assert model.a == 42
    assert model._a == 42
