# -*- coding: utf-8 -*-
#######################################################################
# Name: test_examples
# Purpose: Test that examples run without errors.
# Author: Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# Copyright:
#    (c) 2014-2015 Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#######################################################################
import pytest  # noqa
import os
import sys
import glob
import imp
pyecore = pytest.importorskip("pyecore")  # noqa
import textx


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_examples():

    examples_pat = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                '../../examples_pyecore/*/*.py')

    # Filter out __init__.py
    examples = [f for f in glob.glob(examples_pat) if f != '__init__.py']
    for e in examples:
        print("Running example:", e)
        example_dir = os.path.dirname(e)
        sys.path.insert(0, example_dir)
        (module_name, _) = os.path.splitext(os.path.basename(e))
        (module_file, module_path, desc) = \
            imp.find_module(module_name, [example_dir])

        m = imp.load_module(module_name, module_file, module_path, desc)

        if hasattr(m, 'main'):
            m.main(debug=False)
