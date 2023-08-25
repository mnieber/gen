from pathlib import Path

from moonleap import load_yaml
from titan.types_pkg.typeregistry.resources import TypeRegistry
from titan.typespec.load_type_specs.type_spec_parser import TypeSpecParser


class TestTypeSpecParser:
    def test_parse_type_spec(self):
        type_reg = TypeRegistry()
        parser = TypeSpecParser(type_reg)

        type_spec_dict_fn = Path(__file__).parent / "models.yaml"
        type_spec_dict = load_yaml(str(type_spec_dict_fn))
        parser.parse(type_spec_dict)

        output_fn = Path(__file__).parent / "output.txt"
        with open(str(output_fn), "w") as f:
            log = lambda x: print(str(x), file=f)
            for type_spec in type_reg.type_specs():
                log(type_spec)
                for field_spec in type_spec.field_specs:
                    log("  " + str(field_spec))
