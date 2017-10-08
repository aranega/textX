from __future__ import unicode_literals
import pytest  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx.metamodel import metamodel_from_str
from textx.const import RULE_ABSTRACT, RULE_COMMON


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_json_issue():
    """
    Test wrong rule type in json grammar.
    """
    grammar = """
    File:
        Array | Object
    ;

    Array:
        "[" values*=Value[','] "]"
    ;

    Value:
        PrimitiveValue | Object | Array | NullValue
    ;

    Object:
        "{" members*=Member[','] "}"
    ;

    Member:
        key=STRING ':' value=Value
    ;

    PrimitiveValue:
        val=STRING | val=FLOAT | val=BOOL
    ;

    NullValue:
        val="null"
    ;
    """
    json_mm = metamodel_from_str(grammar)
    assert json_mm['Object']._tx_type is RULE_COMMON
    assert json_mm['Member']._tx_type is RULE_COMMON
    assert json_mm['Array']._tx_type is RULE_COMMON
    assert json_mm['File']._tx_type is RULE_ABSTRACT
    assert json_mm['Value']._tx_type is RULE_ABSTRACT
