from argparse import Namespace

from moonleap.utils.case import l0, sn
from moonleap.utils.inflect import plural


def create_fixture(field_spec):
    name = None
    item_name = sn(l0(field_spec.target))
    is_single = field_spec.field_type in ("fk", "uuid")
    is_multiple = field_spec.field_type in ("relatedSet", "uuid[]")

    if is_single:
        name = item_name
    elif is_multiple:
        name = plural(item_name)
    else:
        raise Exception(f"Unknown field type: {field_spec.field_type}")

    result = Namespace(
        name=name,
        field_spec=field_spec,
        item_name=item_name,
        is_single=is_single,
        is_multiple=is_multiple,
    )

    return result


def define_fixture(root, fixture):
    target_type_spec = fixture.field_spec.target_type_spec
    provided_item_names = [
        l0(sn(x.target)) for x in target_type_spec.get_field_specs(["fk"])
    ]
    django_model_args = [f"{sn(x + 'Id')}={sn(x)}.id" for x in provided_item_names]

    create_random = f"create_random_{fixture.item_name}"

    root.abc(r"@pytest.fixture()")
    fixture_name = sn(fixture.name)
    root.IxI(f"def {fixture_name}", ["self", *provided_item_names], ":")

    if fixture.is_single:
        root.IxI(f"  return {create_random}", django_model_args, "")
    elif fixture.is_multiple:
        root.IxI(f"  x1 = {create_random}", django_model_args, "")
        root.IxI(f"  x2 = {create_random}", django_model_args, "")
        root.abc(r"  return [x1, x2]")
    else:
        raise Exception(f"Cannot define a fixture for: {fixture.field_spec.field_type}")
