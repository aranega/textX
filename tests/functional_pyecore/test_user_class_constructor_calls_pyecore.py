"""
Testing user class constructor call and parent reference.
"""
import pytest  # noqa
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx import metamodel_from_str
from pyecore.ecore import EMetaclass, EAttribute, EInt


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


# Second objects are children of First.
# They should have a parent reference.
grammar = """
First:
    'first' seconds+=Second
    ('A' a+=INT)?
    ('B' b=BOOL)?
    ('C' c=STRING)?
;

Second:
    sec = INT
;

"""


def test_parent_reference():
    """
    Tests that nested objects will have "parent" reference
    that points to containing instance and non-nested
    objects does not have this reference.
    """
    metamodel = metamodel_from_str(grammar)

    model_str = 'first 34 45 7 A 45 65 B true C "dfdf"'
    model = metamodel.model_from_str(model_str)

    assert model.seconds
    for s in model.seconds:
        # Parent reference for each Second instance
        # reffers to the root First instance.
        assert s.parent == model

    # First is not nested so it should not have a parent
    # attribute
    assert not hasattr(model, 'parent')


def test_user_class_constructor_call():
    """
    Tests that user class constructor gets called and
    that parent reference is given in the parameters.
    """
    @EMetaclass
    class Second(object):
        _called = False
        sec = EAttribute(eType=EInt)

        def __init__(self, parent, sec):
            self._called = True
            self.parent = parent
            self.sec = sec

    metamodel = metamodel_from_str(grammar, classes=[Second])

    model_str = 'first 34 45 7 A 45 65 B true C "dfdf"'
    model = metamodel.model_from_str(model_str)

    assert model.seconds
    for s in model.seconds:
        assert s._called
        assert s.parent == model
        assert s.sec in [34, 45, 7]
