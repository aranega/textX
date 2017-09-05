from textx.metamodel import metamodel_from_str
from pyecore.ecore import *
from textx.export import metamodel_export

grammar = """
StateMachine:
    'events'
        events+=Event
    'end'

    ('resetEvents'
        resetEvents+=[Event|SMID]
    'end')?

    'commands'
        commands+=Command
    'end'

    states+=State
;

Keyword:
    'end' | 'events' | 'resetEvents' | 'state' | 'actions'
;

Event:
    name=SMID code=ID
;

Command:
    name=SMID code=ID
;

State:
    'state' name=ID
        ('actions' '{' actions+=[Command] '}')?
        transitions+=Transition
    'end'
;

Transition:
    event=[Event|SMID] '=>' to_state=[State]
;

SMID:
    !Keyword ID
;

Comment:
    /\/\*(.|\n)*?\*\//
;
"""

mm = metamodel_from_str(grammar)
# for name, mc in mm.namespaces[None].items():
#     if isinstance(mc, EClass):
#         print(mc, mc.eStructuralFeatures)

metamodel_export(mm, 'test.dot')

program = mm.model_from_str("""
events
  passTrough    GTPT
  coinInserted  CINS
end

commands
  unlockGate    GTUN
  lockGate      GTLK
end

state locked
  actions {lockGate}
  coinInserted => unlocked
end

state unlocked
  actions {unlockGate}
  passTrough => locked
end
""")

for x in program.eAllContents():
    if hasattr(x, 'name'):
        print(x.name, x.eClass, x)

print(program.states[0].transitions[0].event)
