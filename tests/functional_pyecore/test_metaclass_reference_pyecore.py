import pytest
import os
pyecore = pytest.importorskip("pyecore")  # noqa
from textx.metamodel import metamodel_from_str, metamodel_from_file
from pyecore.ecore import EMetaclass
import textx


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


grammar = """
First:
    'first' seconds+=Second
;

Second:
    value=INT|value=STRING
;

"""


def test_metaclass_ref():
    metamodel = metamodel_from_str(grammar)
    First = metamodel['First']
    Second = metamodel['Second']

    model = metamodel.model_from_str('first 45 "test" 12')

    assert model.eClass is First
    assert all(x.eClass is Second for x in model.seconds)


def test_metaclass_user_class():
    """
    User supplied meta class.
    """
    @EMetaclass
    class First(object):
        def __init__(self, seconds=None):
            self.seconds = seconds

    metamodel = metamodel_from_str(grammar, classes=[First])

    model = metamodel.model_from_str('first 45 12')
    assert type(model) is First


@pytest.mark.parametrize("filename", ["first.tx", "first_new.tx"])
def test_metaclass_relative_paths(filename):
    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'test_import',
                                          'importoverride', filename))
    Third = mm['Third']
    ThirdMasked = mm['relative.third.Third']
    assert Third is not ThirdMasked

    model = mm.model_from_str('first 12 45 third "abc" "xyz"')
    inner_second = model.first[0]

    assert all(x.eClass is ThirdMasked for x in inner_second.second)
    assert all(x.eClass is Third for x in model.third)


def test_diamond_import():
    """
    Test that diamond rule import results in the same class.
    """

    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'test_import',
                                          'importoverride',
                                          'first_diamond.tx'))
    First = mm['First']
    MyDiamondRule = mm['diamond.last.MyDiamondRule']

    model = mm.model_from_str('second 12 45 third 4 5')

    assert model.eClass is First
    assert all(x.diamond.eClass is MyDiamondRule for x in model.seconds)
    assert all(x.diamond.eClass is MyDiamondRule for x in model.thirds)
