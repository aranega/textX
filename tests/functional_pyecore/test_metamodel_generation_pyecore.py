# -*- coding: utf-8 -*-

import pytest  # noqa
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
pyecore = pytest.importorskip("pyecore")  # noqa
import textx
from pyecoregen.ecore import EcoreGenerator
from pyecore.resources import URI
import pyecore.ecore as Ecore
import importlib


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


grammar = """
First:
    dummy=INT
    ('first' seconds+=Second)?
    ('A' a=INT)?
    ('B' b=BOOL)?
    ('C' c=STRING)?
    d?='boolasgn'
    ('F' f=FLOAT)?
;

Second:
    'a' name=STRING
;

"""


@pytest.fixture('module')
def cwd_module_dir():
    """Change current directory to this module's folder to access inputs and
       write outputs."""
    import os
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    yield
    os.chdir(cwd)


@pytest.fixture(scope='module')
def pygen_output_dir(cwd_module_dir):
    import shutil
    """Return an empty output directory, part of syspath to allow
       importing generated code."""
    path = 'output'
    shutil.rmtree(path, ignore_errors=True)
    sys.path.append(path)
    yield path
    sys.path.remove(path)
    shutil.rmtree(path, ignore_errors=False)


def generate_meta_model(model, output_dir, *, user_module=None,
                        auto_register_package=None):
    generator = EcoreGenerator(user_module=user_module,
                               auto_register_package=auto_register_package)
    generator.generate(model, output_dir)
    return importlib.import_module(model.name)


def test_generate_single_metamodel(pygen_output_dir):
    metamodel = textx.metamodel_from_str(grammar)
    mm = generate_meta_model(metamodel, pygen_output_dir,
                             auto_register_package=True)

    assert mm.First
    assert isinstance(mm.First.seconds, Ecore.EReference)
    assert mm.Second
    assert mm.First.seconds.eType is mm.Second
    assert mm.First.d.eType is Ecore.EBoolean
