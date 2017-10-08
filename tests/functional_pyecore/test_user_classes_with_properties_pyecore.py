import pytest  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx.metamodel import metamodel_from_str
from pyecore.ecore import EMetaclass, EInt, EAttribute


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


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
