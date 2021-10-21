from moonleap.parser.block import Block
from moonleap.parser.term import Term
from moonleap.resource import Resource

_lut = dict()


class NamedResource(Resource):
    pass


def constructor(self, term: Term, block: Block):
    super(NamedResource, self).__init__()
    self.name = None
    self.typ = None


def named(klass, base_klass=NamedResource):
    named_klass_name = f"Named{klass.__name__}"
    result = _lut.get(named_klass_name)

    if not result:
        result = type(named_klass_name, (base_klass,), {"__init__": constructor})
        _lut[named_klass_name] = result

    return result
