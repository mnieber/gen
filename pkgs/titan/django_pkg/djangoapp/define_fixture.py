from moonleap.utils.case import l0, sn
from moonleap.utils.inflect import plural


def define_fixture(root, field_spec):
    is_single = field_spec.field_type in ("fk", "uuid")
    is_multiple = field_spec.field_type in ("relatedSet", "uuid[]")

    target_type_spec = field_spec.target_type_spec
    provided_item_names = [
        l0(x.target) for x in target_type_spec.get_field_specs(["fk"])
    ]
    django_model_args = [f"{sn(x + 'Id')}={sn(x)}.id" for x in provided_item_names]

    item_name = sn(l0(field_spec.target))
    if is_multiple:
        item_name = plural(item_name)
    create_random = f"create_random_{item_name}"

    root.abc(r"@pytest.fixture()")
    root.IxI(f"def {item_name}", ["self", *provided_item_names], ":")

    if is_single:
        root.IxI(f"  return {create_random}", django_model_args, "")
    elif is_multiple:
        root.IxI(f"  x1 = {create_random}", django_model_args, "")
        root.IxI(f"  x2 = {create_random}", django_model_args, "")
        root.abc(r"  return [x1, x2]")
    else:
        raise Exception(f"Cannot define a fixture for: {field_spec.field_type}")
