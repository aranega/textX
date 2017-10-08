from __future__ import unicode_literals
import pytest  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx.metamodel import metamodel_from_str


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_issue_33_parentheses():

    grammar = """
    Method:
        'func('  (params+=Parameter[','])?  ')'
    ;
    Parameter:
        (type=ID name=ID)  |  name=ID
    ;
    """

    meta_model = metamodel_from_str(grammar)
    model = meta_model.model_from_str(
        """
        func( a b, c )
        """
    )
    assert model
    assert model.params[0].type == 'a'
    assert model.params[0].name == 'b'

    assert model.params[1].type == ''
    assert model.params[1].name == 'c'


def test_issue_33_alternatives():
    grammar = """
    Method:
        'func('  (params+=Parameter[','])?  ')'
    ;
    Parameter:
        type=ID name=ID  |  name=ID
    ;
    """

    meta_model = metamodel_from_str(grammar)
    model = meta_model.model_from_str(
        """
        func( a b, c )
        """
    )
    assert model
    assert model.params[0].type == 'a'
    assert model.params[0].name == 'b'

    assert model.params[1].type == ''
    assert model.params[1].name == 'c'


def test_issue_33_alternatives_with_arbitrary_named_attr():
    grammar = """
    Method:
        'func('  (params+=Parameter[','])?  ')'
    ;
    Parameter:
        type=ID my_name=ID  |  my_name=ID
    ;
    """

    meta_model = metamodel_from_str(grammar)
    model = meta_model.model_from_str(
        """
        func( a b, c )
        """
    )
    assert model
    assert model.params[0].type == 'a'
    assert model.params[0].my_name == 'b'

    assert model.params[1].type == ''
    assert model.params[1].my_name == 'c'
