# -*- coding: utf-8 -*-

import pytest  # noqa
import sys
pytestmark = pytest.mark.skipif(sys.version_info[0] < 3,
                                reason="pyecore is not Python 2 compatible")  # noqa
ecore = pytest.importorskip("pyecore.ecore")  # noqa
import textx
from textx import metamodel_from_str
from textx.lang import TextXSyntaxError


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
    assert IsEnum.name == 'IsEnum'
    assert all((x in IsEnum for x in ("keyword1", "keyword2", "keyword3")))

    IsNotEnum = mm['IsNotEnum']
    assert IsNotEnum.name == 'IsNotEnum'
    assert isinstance(IsNotEnum, ecore.EClass)

    StillNotEnum = mm['StillNotEnum']
    assert StillNotEnum.name == 'StillNotEnum'
    assert isinstance(StillNotEnum, ecore.EClass)

    NotEnumAgain = mm['NotEnumAgain']
    assert isinstance(NotEnumAgain, ecore.EDataType)
    assert NotEnumAgain.name == 'NotEnumAgain'

    SubEnum = mm['SubEnum']
    assert isinstance(SubEnum, ecore.EEnum)
    assert SubEnum.name == 'SubEnum'
    assert all((x in IsEnum for x in ("keyword1", "keyword2")))


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
    assert IsObjectDatatype.name == 'IsObjectDatatype'
    assert IsObjectDatatype.eType == object

    IsIntDatatype = mm['IsIntDatatype']
    assert isinstance(IsIntDatatype, ecore.EDataType)
    assert IsIntDatatype.name == 'IsIntDatatype'
    assert IsIntDatatype.eType == int

    IsIdDatatype = mm['IsIdDatatype']
    assert isinstance(IsIdDatatype, ecore.EDataType)
    assert IsIdDatatype.name == 'IsIdDatatype'
    assert IsIdDatatype.eType == str

    IsAlsoDatatype = mm['IsAlsoDatatype']
    assert isinstance(IsAlsoDatatype, ecore.EDataType)
    IsAlsoDatatype = mm['IsAlsoDatatype']
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

    ID = mm['ID']
    INT = mm['INT']
    IsEClass = mm['IsEClass']
    assert isinstance(IsEClass, ecore.EClass)
    assert IsEClass.name == 'IsEClass'
    assert IsEClass.abstract is False

    AbstractEClass = mm['AbstractEClass']
    OtherEClass = mm['OtherEClass']
    assert isinstance(AbstractEClass, ecore.EClass)
    assert isinstance(OtherEClass, ecore.EClass)
    assert AbstractEClass.abstract
    assert OtherEClass.abstract
    assert AbstractEClass.name == 'AbstractEClass'
    assert OtherEClass.name == 'OtherEClass'

    assert len(IsEClass.eSuperTypes) == 2
    assert AbstractEClass in IsEClass.eSuperTypes
    assert OtherEClass in IsEClass.eSuperTypes

    assert len(IsEClass.eAttributes) == 2
    nameFeature, yearFeature = IsEClass.eStructuralFeatures
    assert nameFeature.name == 'name' and nameFeature.eType is ID
    assert yearFeature.name == 'year' and yearFeature.eType is INT


def test_incompatible_rules():
    """
    Test that 'mixed' rules raises errors
    """

    grammar = """
    A: B | C;
    B: 'enumeration';
    C: value=INT;
    """
    with pytest.raises(TextXSyntaxError):
        metamodel_from_str(grammar)
