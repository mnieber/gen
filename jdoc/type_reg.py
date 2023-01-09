from jdoc.scenario import *


@dataclass
class TypeSpec(Resource):
    pass


@dataclass
class TypeReg(Entity):
    type_specs: list[TypeSpec] = field(default_factory=list)

    def load_type_specs(self):
        pass


global_type_reg = TypeReg()
