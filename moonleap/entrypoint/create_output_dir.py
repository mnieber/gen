import os


def create_output_dir(output_dir, references_config):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for output_subdir_name, reference_dir in references_config.items():
        if not os.path.exists(reference_dir):
            raise Exception(f"Reference dir not found: {reference_dir}")
        base_output_dir = os.path.join(output_dir, os.path.dirname(output_subdir_name))
        if not os.path.exists(base_output_dir):
            os.makedirs(base_output_dir)
        symlink_fn = os.path.join(output_dir, output_subdir_name)

        if os.path.exists(symlink_fn):
            is_symlink_fn_targetting_reference_dir = (
                os.path.islink(symlink_fn) and os.readlink(symlink_fn) == reference_dir
            )
            if not is_symlink_fn_targetting_reference_dir:
                raise Exception(
                    f"Output dir already exists and is not a symlink to the reference dir: {symlink_fn}"
                )
        else:
            os.symlink(reference_dir, symlink_fn)
