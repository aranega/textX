from os.path import join, dirname
from textx.metamodel import metamodel_from_str
from textx.export import metamodel_export, model_export
from pyecore.ecore import EObject, EMetaclass, EReference, EAttribute, \
                            ENativeType, EEnum

grammar = '''
Calc: assignments*=Assignment expression=Expression;
Assignment: variable=ID '=' expression=Expression ';';
Expression: op=Term (op=PlusOrMinus op=Term)* ;
PlusOrMinus: '+' | '-';
Term: op=Factor (op=MulOrDiv op=Factor)*;
MulOrDiv: '*' | '/' ;
Factor: (sign=PlusOrMinus)?  op=Operand;
Operand: op=NUMBER | op=ID | ('(' op=Expression ')');
'''

# Global variable namespace
namespace = {}

PlusOrMinus = EEnum('PlusOrMinus', literals=('+', '-'))
MultOrDiv = EEnum('MultOrDiv', literals=('*', '/'))


@EMetaclass
class Calc(object):
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
    op = EReference(eType=EObject, upper=-1)

    def __init__(self, **kwargs):

        # textX will pass in parent attribute used for parent-child
        # relationships. We can use it if we want to.
        self.parent = kwargs.get('parent', None)

        # We have 'op' attribute in all grammar rules
        self.op = kwargs['op']

        super(ExpressionElement, self).__init__()


class Factor(ExpressionElement):
    sign = EAttribute(eType=PlusOrMinus)

    def __init__(self, **kwargs):
        self.sign = kwargs.pop('sign', '+')
        super(Factor, self).__init__(**kwargs)

    @property
    def value(self):
        value = self.op.value
        return -value if self.sign == '-' else value


class Term(ExpressionElement):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '*':
                ret *= operand.value
            else:
                ret /= operand.value
        return ret


class Expression(ExpressionElement):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '+':
                ret += operand.value
            else:
                ret -= operand.value
        return ret


Calc.expression = EReference('expression', Expression)


class Operand(ExpressionElement):
    op = EAttribute(eType=ENativeType)

    @property
    def value(self):
        op = self.op
        if type(op) in {int, float}:
            return op
        elif isinstance(op, ExpressionElement):
            return op.value
        elif op in namespace:
            return namespace[op]
        else:
            raise Exception('Unknown variable "{}" at position {}'
                            .format(op, self._tx_position))


Factor.op = EReference('op', Operand)


def main(debug=False):

    calc_mm = metamodel_from_str(grammar,
                                 classes=[Calc, Expression, Term, Factor,
                                          Operand, PlusOrMinus, MultOrDiv],
                                 debug=debug)

    this_folder = dirname(__file__)
    if debug:
        metamodel_export(calc_mm, join(this_folder, 'calc_metamodel.dot'))

    input_expr = '''
        a = 10;
        b = 2 * a + 17;
        -(4-1)*a+(2+4.67)+b*5.89/(.2+7)
    '''

    model = calc_mm.model_from_str(input_expr)

    if debug:
        model_export(model, join(this_folder, 'calc_model.dot'))

    # Getting value property from the Calc instance will start evaluation.
    result = model.value

    assert (model.value - 6.93805555) < 0.0001
    print("Result is", result)


if __name__ == '__main__':
    main()