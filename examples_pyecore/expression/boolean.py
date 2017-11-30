from os.path import join, dirname
from textx import metamodel_from_str
from textx.pyecore import enable_pyecore_support
from textx.export import metamodel_export, model_export
from pyecore.ecore import EObject, EMetaclass, EReference, EAttribute, \
                            ENativeType, EBoolean

enable_pyecore_support()

grammar = '''
Bool: assignments*=Assignment expression=Or;
Assignment: variable=ID '=' expression=Or';';
Or: op=And ('or' op=And)*;
And: op=Not ('and' op=Not)*;
Not: _not?='not' op=Operand;
Operand: op=BOOL | op=ID | ( '(' op=Or ')' );
'''

# Global variable namespace
namespace = {}


@EMetaclass
class Bool(object):
    assignments = EReference(eType=EObject, upper=-1)
    expression = EReference()

    def __init__(self, **kwargs):
        self.assignments = kwargs.pop('assignments')
        self.expression = kwargs.pop('expression')

    @property
    def value(self):
        # Evaluate variables in the order of definition
        for a in self.assignments:
            namespace[a.variable] = a.expression.value
        return self.expression.value


@EMetaclass
class ExpressionElement(object):
    def __init__(self, **kwargs):

        # textX will pass in parent attribute used for parent-child
        # relationships. We can use it if we want to.
        self.parent = kwargs.get('parent', None)

        # We have 'op' attribute in all grammar rules
        self.op = kwargs['op']

        super(ExpressionElement, self).__init__()


class Or(ExpressionElement):
    op = EReference(upper=-1)

    @property
    def value(self):
        ret = self.op[0].value
        for operand in self.op[1:]:
                ret = ret or operand.value
        return ret


Bool.expression.eType = Or


class And(ExpressionElement):
    op = EReference(upper=-1)

    @property
    def value(self):
        ret = self.op[0].value
        for operand in self.op[1:]:
            ret = ret and operand.value
        return ret


Or.op.eType = And


class Not(ExpressionElement):
    _not = EAttribute(eType=EBoolean)
    op = EReference()

    def __init__(self, **kwargs):
        self._not = kwargs.pop('_not')
        super(Not, self).__init__(**kwargs)

    @property
    def value(self):
        ret = self.op.value
        return not ret if self._not else ret


And.op.eType = Not


class Operand(ExpressionElement):
    op = EAttribute(eType=ENativeType)

    @property
    def value(self):
        op = self.op
        if type(op) is bool:
            return op
        elif op in namespace:
            return namespace[op]
        else:
            raise Exception('Unknown variable "{}" at position {}'
                            .format(op, self._tx_position))


Not.op.eType = Operand


def main(debug=False):

    bool_mm = metamodel_from_str(grammar,
                                 classes=[Bool, Or, And, Not, Operand],
                                 ignore_case=True,
                                 debug=debug)

    this_folder = dirname(__file__)
    if debug:
        metamodel_export(bool_mm, join(this_folder, 'bool_metamodel.dot'))

    input_expr = '''
        a = true;
        b = not a and true;
        a and false or not b
    '''

    model = bool_mm.model_from_str(input_expr)

    if debug:
        model_export(model, join(this_folder, 'bool_model.dot'))

    # Getting value property from the Bool instance will start evaluation.
    result = model.value

    assert model.value is True
    print("Result is", result)


if __name__ == '__main__':
    main()
