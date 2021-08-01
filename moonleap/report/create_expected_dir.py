import os


def create_expected_dir(expected_dir, references_config):
    if not os.path.exists(expected_dir):
        os.makedirs(expected_dir)

    for reference_dir_name, reference_dir in references_config.items():
        symlink_fn = os.path.join(expected_dir, reference_dir_name)
        if os.path.exists(symlink_fn) or os.path.islink(symlink_fn):
            if not os.path.islink(symlink_fn):
                raise Exception(
                    f"Cannot prepare {reference_dir} because it contains {symlink_fn} "
                    + "which is not a symlink."
                )
            os.unlink(symlink_fn)
        os.symlink(reference_dir, symlink_fn)
