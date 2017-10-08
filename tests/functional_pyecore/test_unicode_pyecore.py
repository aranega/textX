# -*- coding: utf-8 -*-
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


def test_unicode_grammar_from_string():
    """
    Test grammar with unicode char given in grammar string.
    """

    grammar = """
    First:
        'first' a = Second
    ;

    Second:
        "Ω"|"±"|"♪"
    ;

    """

    metamodel = metamodel_from_str(grammar)
    assert metamodel
