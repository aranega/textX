# -*- coding: utf-8 -*-

import pytest  # noqa
ecore = pytest.importorskip("pyecore.ecore")  # noqa
import textx
from textx.metamodel import metamodel_from_str


@pytest.fixture(scope="module")
def enable_pyecore_support():
    textx.enable_pyecore_support()
    yield
    textx.enable_pyecore_support(enable=False)


pytestmark = pytest.mark.usefixtures("enable_pyecore_support")


def test_enum_detection():
    """
    Test that enumeration are properly detected
    """

    grammar = """
    IsEnum: "keyword1" | "keyword2" | "keyword3";
    IsNotEnum: val="keyword1" | val="keyword2" | val="keyword3";
    StillNotEnum: val="keyword1" | "keyword2" | "keyword3";

    // identified as EDatatype with object type
    NotEnumAgain: SubEnum | SubEnum2;

    // this is an enumeration
    SubEnum: "keyword1" | "keyword2";
    SubEnum2: "keyword3" | "keyword4";
    """

    mm = metamodel_from_str(grammar)

    IsEnum = mm['IsEnum']
    assert isinstance(IsEnum, ecore.EEnum)

    IsNotEnum = mm['IsNotEnum']
    assert isinstance(IsNotEnum, ecore.EClass)

    StillNotEnum = mm['StillNotEnum']
    assert isinstance(StillNotEnum, ecore.EClass)

    NotEnumAgain = mm['NotEnumAgain']
    assert isinstance(NotEnumAgain, ecore.EDataType)

    SubEnum = mm['SubEnum']
    assert isinstance(SubEnum, ecore.EEnum)


def test_datatype_detection():
    """
    Test that datatypes are properly detected
    """

    grammar = """
    IsObjectDatatype: INT | STRING | ID;
    IsIntDatatype: INT;
    IsIdDatatype: ID;
    IsAlsoDatatype: SubDT1 | SubDT2;
    SubDT1: INT;
    SubDT2: STRING;
    """

    mm = metamodel_from_str(grammar)

    IsObjectDatatype = mm['IsObjectDatatype']
    assert isinstance(IsObjectDatatype, ecore.EDataType)
    assert IsObjectDatatype.eType == object

    IsIntDatatype = mm['IsIntDatatype']
    assert isinstance(IsIntDatatype, ecore.EDataType)
    assert IsIntDatatype.eType == int

    IsIdDatatype = mm['IsIdDatatype']
    assert isinstance(IsIdDatatype, ecore.EDataType)
    assert IsIdDatatype.eType == str

    IsAlsoDatatype = mm['IsAlsoDatatype']
    assert isinstance(IsAlsoDatatype, ecore.EDataType)
    assert IsAlsoDatatype.eType == object


def test_eclass_detection():
    """
    Test that datatypes are properly detected
    """

    grammar = """
    AbstractEClass: IsEClass;
    OtherEClass: IsEClass;  // multiple inheritance
    IsEClass: 'name' name=ID ',' 'year' year=INT;
    """

    mm = metamodel_from_str(grammar)

    IsEClass = mm['IsEClass']
    assert isinstance(IsEClass, ecore.EClass)

    AbstractEClass = mm['AbstractEClass']
    OtherEClass = mm['OtherEClass']
    assert isinstance(AbstractEClass, ecore.EClass)
    assert isinstance(OtherEClass, ecore.EClass)
    assert AbstractEClass.abstract
    assert OtherEClass.abstract

    assert len(IsEClass.eSuperTypes) == 2
    assert AbstractEClass in IsEClass.eSuperTypes
    assert OtherEClass in IsEClass.eSuperTypes
