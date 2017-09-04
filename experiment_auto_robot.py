from textx.metamodel import metamodel_from_str
from pyecore.ecore import *

grammar = """
Program:
  'begin'
    commands*=Command
  'end'
;

Command:
  InitialCommand | MoveCommand
;

InitialCommand:
  'initial' x=INT ',' y=INT
;

MoveCommand:
  direction=Direction (steps=INT)?
;

Direction:
  "up"|"down"|"left"|"right"
;

Comment:
  /\/\/.*$/
;
"""

mm = metamodel_from_str(grammar)

program = mm.model_from_str("""
// test
begin
    initial 3, 1
    up 4
    left 9
    down
    right 1
end
""")

for command in program.commands:
    if hasattr(command, 'x'):
        print('start at {}, {}'.format(command.x, command.y))
    else:
        print('walk {} for {} steps'.format(command.direction, command.steps))

for c in program.eAllContents():
    print(c.eClass, c)
