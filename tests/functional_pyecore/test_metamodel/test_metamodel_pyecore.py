import pytest  # noqa
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
import os
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx import metamodel_from_str, metamodel_from_file


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
    value=INT
;

"""


def test_textx_metaclass_repr():
    """
    Test metaclass __repr__
    """

    metamodel = metamodel_from_str(grammar)
    assert repr(metamodel['First'])
    # assert '<textx:First class at' in repr(metamodel['First'])


def test_textx_metaclass_instance_repr():
    """
    Test metaclass instance __repr__
    """

    metamodel = metamodel_from_str(grammar)
    model = metamodel.model_from_str('first 42')
    assert repr(model)
    # assert '<textx:First instance at' in repr(model)


def test_textx_imported_metaclass_repr():
    """
    Test imported metaclass __repr__ uses fqn.
    """

    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'import',
                                          'first_diamond.tx'))
    MyDiamondRule = mm['diamond.last.MyDiamondRule']

    assert repr(MyDiamondRule)
    # assert '<textx:diamond.last.MyDiamondRule class at' in repr(MyDiamondRule)


def test_textx_imported_metaclass_instance_repr():
    """
    Test imported metaclass instance __repr__ uses fqn.
    """

    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'import',
                                          'first_diamond.tx'))
    model = mm.model_from_str('second 42 11 third 42')

    assert repr(model.seconds[0].diamond)
    # assert '<textx:diamond.last.MyDiamondRule instance at' \
    #     in repr(model.seconds[0].diamond)


def test_textx_imported_metaclass_repr_same_level_import():
    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'import',
                                          'repr',
                                          'first_repr.tx'))
    model = mm.model_from_str('second 42')

    assert repr(model.seconds[0].thirds[0])
    # assert '<textx:third_repr.Third instance at' \
    #     in repr(model.seconds[0].thirds[0])
