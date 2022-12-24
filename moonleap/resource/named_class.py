from moonleap.resource import Resource

_lut = dict()


class NamedResource(Resource):
    def __str__(self):
        return f"Named {self.typ}"

    def __repr__(self):
        return f"Named {self.typ}"


def constructor(self):
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
