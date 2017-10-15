from __future__ import unicode_literals
import pytest
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from textx.metamodel import metamodel_from_str
from textx.exceptions import TextXSyntaxError


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_noskipws():
    """
    Test 'noskipws' rule modifier.
    """
    grammar = """
    Rule:
        'entity' name=ID /\s*/ call=Rule2;
    Rule2[noskipws]:
        'first' 'second';
    """
    metamodel = metamodel_from_str(grammar)

    # Rule2 disables ws skipping so this will not parse.
    with pytest.raises(TextXSyntaxError):
        metamodel.model_from_str("entity Person first second")

    # This will parse.
    metamodel.model_from_str("entity Person firstsecond")


def test_skipws():
    """
    Test 'skipws' rule modifier.
    """
    grammar = """
    Rule:
        'entity' name=ID call=Rule2;
    Rule2[skipws]:
        'first' 'second';
    """

    # Change default behavior
    metamodel = metamodel_from_str(grammar, skipws=False)

    # ws skipping is disabled globally but Rule2 enables ws skipping
    # so this will not parse.
    with pytest.raises(TextXSyntaxError):
        metamodel.model_from_str("entity Person first second")

    # This will parse.
    metamodel.model_from_str("entityPerson first  second")


def test_ws():
    """
    Test 'ws' rule modifier.
    """
    grammar = """
    Rule:
        'entity' name=ID /\s*/ call=Rule2;
    Rule2[ws='\n']:
        'first' 'second';
    """
    metamodel = metamodel_from_str(grammar)

    # Rule2 redefines ws to be newline only so
    # the space between 'first' and 'second' cannot
    # be skipped.
    with pytest.raises(TextXSyntaxError):
        metamodel.model_from_str("entity Person first second")

    # This will parse.
    metamodel.model_from_str("entity Person first\nsecond")

    # In this variant we will skip spaces and tabs but not newlines.
    grammar = """
    Rule:
        'entity' name=ID /\s*/ call=Rule2;
    Rule2[ws=' \t']:
        'first' 'second';
    """
    metamodel = metamodel_from_str(grammar)

    # This will not parse
    with pytest.raises(TextXSyntaxError):
        metamodel.model_from_str("entity Person first\n second")

    # But this will
    metamodel.model_from_str("entity Person first\t \tsecond")
    metamodel.model_from_str("entity Person \nfirst\t \tsecond")


def test_skipws_ws():
    """
    Test 'skipws' and 'ws'rule modifier in combination.
    """

    grammar = """
    Rule:
        'entity' name=ID call=Rule2;
    Rule2[skipws, ws=' \t']:
        'first' 'second';
    """

    # Change default behavior
    metamodel = metamodel_from_str(grammar, skipws=False)

    # Skipping of ws is disabled globally but Rule2 overrides that.
    with pytest.raises(TextXSyntaxError):
        metamodel.model_from_str("entity Person first second")

    # This will parse.
    metamodel.model_from_str("entityPerson first\t\t \t second")
