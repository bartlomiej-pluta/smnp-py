from smnp.library.model import Function
from smnp.library.signature import signature, ofType
from smnp.type.model import Type

_signature = signature(ofType(Type.NOTE), ofType(Type.INTEGER))
def _function(env, note, duration):
    return Type.note(note.value.withDuration(duration.value))


function = Function(_signature, _function, 'withDuration')