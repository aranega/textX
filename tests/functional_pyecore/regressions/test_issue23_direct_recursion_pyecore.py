from __future__ import unicode_literals
import pytest  # noqa
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx

from textx.metamodel import metamodel_from_str
from textx.const import RULE_COMMON, RULE_ABSTRACT, RULE_MATCH


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_issue_23():
    """
    Test that rule types are correctly determined on direct recursion.
    """

    grammar = """
    List: members+=Value;
    Value: ('{' List '}') | Identifier;
    Identifier: val=ID;
    """
    mm = metamodel_from_str(grammar)

    assert mm['List']._tx_type is RULE_COMMON
    assert mm['Value']._tx_type is RULE_ABSTRACT
    assert mm['Value']._tx_inh_by == [mm['List'], mm['Identifier']]

    grammar = """
    List: '{' members+=Value '}';
    Value: ID;
    """
    mm = metamodel_from_str(grammar)

    assert mm['List']._tx_type is RULE_COMMON
    assert mm['Value']._tx_type is RULE_MATCH

    grammar = """
    ListSyntax: '{' List '}';
    List: members+=Value;
    Value: ListSyntax | Identifier;
    Identifier: val=ID;
    """
    mm = metamodel_from_str(grammar)

    assert mm['ListSyntax']._tx_type is RULE_ABSTRACT
    assert mm['ListSyntax']._tx_inh_by == [mm['List']]
    assert mm['List']._tx_type is RULE_COMMON
    assert mm['Value']._tx_type is RULE_ABSTRACT
    assert mm['Value']._tx_inh_by == [mm['ListSyntax'], mm['Identifier']]
