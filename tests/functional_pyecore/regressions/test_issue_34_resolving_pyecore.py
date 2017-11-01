from __future__ import unicode_literals
import pytest  # noqa
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx.metamodel import metamodel_from_str


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_issue_34_resolving():
    """An issue in resolving a list of objects of different types.

    In the grammar below, attribute `values` in `FormulaExp` collect STRING
    instances which leads textX to deduce the type of this attribute to be list
    of STRING objects. Thus, object reference resolving does not consider the
    `values` list.

    In the new version textX will deduce type OBJECT if different types are
    used in multiple assignments.

    """

    grammar = """
    Expression:
        atts+=Attribute[','] 'formula' form=Formula
    ;
    Formula:
        value=FormulaExp
    ;


    FormulaExp:
        values=Cond
        | ( values='(' values=Formula values=')' )
    ;

    Cond:
        attribute = [Attribute|attr_id] '<' values=STRING
    ;

    attr_id:
        /attr_[a-f0-9]+/
    ;

    Attribute:
        name = attr_id
    ;
    """

    meta_model = metamodel_from_str(grammar)
    model = meta_model.model_from_str(
        "attr_123, attr_444 formula attr_123 < 'aa'")
    assert type(model.form.value.values[0].attribute).__name__ == 'Attribute'
    assert model.form.value.values[0].attribute.name == 'attr_123'