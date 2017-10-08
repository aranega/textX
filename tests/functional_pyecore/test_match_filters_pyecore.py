from __future__ import unicode_literals
import pytest  # noqa
import sys
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx.metamodel import metamodel_from_str

if sys.version < '3':
    text = unicode  # noqa
else:
    text = str


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_match_filter_simple_match_rule():
    grammar = """
    First:
        a=MyFloat 'end'
    ;
    MyFloat:
        /\d+\.(\d+)?/
    ;
    """
    model = '3. end'

    mm = metamodel_from_str(grammar)
    m = mm.model_from_str(model)
    assert type(m.a) is text

    filters = {
        'MyFloat': lambda x: float(x)
    }
    print('filters')
    mm = metamodel_from_str(grammar, match_filters=filters)
    m = mm.model_from_str(model)

    assert type(m.a) is float


def test_match_filter_sequence_match_rule():

    grammar = """
    First:
        i=MyFixedInt 'end'
    ;
    MyFixedInt:
    '0' '0' '04'
    ;
    """

    model = '0004 end'

    mm = metamodel_from_str(grammar)
    m = mm.model_from_str(model)
    assert type(m.i) is text

    filters = {
        'MyFixedInt': lambda x: int(x)
    }
    mm = metamodel_from_str(grammar, match_filters=filters)
    m = mm.model_from_str(model)

    assert type(m.i) is int


@pytest.mark.skip(reason="In PyEcore, typing is performed at runtime. Thus "
                  "a float cannot be stored in an INT.")
def test_base_filter_override():
    grammar = """
    First:
        'begin' i=INT 'end'
    ;
    """

    filters = {
        'INT': lambda x: float(x)
    }
    mm = metamodel_from_str(grammar, match_filters=filters)
    m = mm.model_from_str('begin 34 end')

    assert type(m.i) is float
