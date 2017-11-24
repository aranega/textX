import pytest  # noqa
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx import metamodel_from_str
from pyecore.ecore import EMetaclass, EAttribute, EString, EBoolean, EInt, \
                            ECollection


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


grammar = """
First:
    'first' seconds+=Second
    ('A' a+=INT)?
    ('B' b=BOOL)?
    ('C' c=STRING)?
;

Second:
    INT|STRING
;

"""


def test_user_class():
    """
    User supplied meta class.
    """
    @EMetaclass
    class First(object):
        "User class."
        a = EAttribute(eType=EInt, upper=-1)
        b = EAttribute(eType=EBoolean)
        c = EAttribute(eType=EString)

        def __init__(self, seconds, a, b, c):
            "Constructor must be without parameters."
            # Testing that additional attributes
            # are preserved.
            self.some_attr = 1
            self.seconds = seconds
            self.a = a
            self.b = b
            self.c = c

    modelstr = """
    first 34 45 65 "sdf" 45
    """

    mm = metamodel_from_str(grammar)
    model = mm.model_from_str(modelstr)
    # Test that generic First class is created
    assert type(model).__name__ == "First"
    assert type(model) is not First

    mm = metamodel_from_str(grammar, classes=[First])
    model = mm.model_from_str(modelstr)
    # Test that user class is instantiated
    assert type(model).__name__ == "First"
    assert type(model) is First
    # Check default attributes
    assert isinstance(model.a, ECollection)
    assert model.a == []
    assert type(model.b) is bool
    assert model.b is False

    # Check additional attributes
    assert model.some_attr == 1
