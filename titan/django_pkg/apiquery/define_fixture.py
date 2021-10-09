from moonleap.utils.case import sn


def define_fixture(root, field_spec):
    target_type_spec = field_spec.target_type_spec
    provided_item_names = [x.target for x in target_type_spec.get_field_specs(["fk"])]
    django_model_args = [f"{sn(x + 'Id')}={sn(x)}.id" for x in provided_item_names]
    create_random = f"create_random_{sn(field_spec.target)}"

    root.abc(r"@pytest.fixture()")
    root.IxI(f"def {sn(field_spec.name)}", ["self", *provided_item_names], ":")

    if field_spec.field_type == "fk":
        root.IxI(f"  return {create_random}", django_model_args, "")
    elif field_spec.field_type == "relatedSet":
        root.IxI(f"  x1 = {create_random}", django_model_args, "")
        root.IxI(f"  x2 = {create_random}", django_model_args, "")
        root.abc(r"  return [x1, x2]")
    else:
        raise Exception(f"Cannot define a fixture for: {field_spec.field_type}")
