import os

from moonleap.render.settings import get_settings


def create_expected_dir(expected_dir):
    if not os.path.exists(expected_dir):
        os.mkdir(expected_dir)

    for reference_dir_name, reference_dir in get_settings()["references"].items():
        symlink_fn = os.path.join(expected_dir, reference_dir_name)
        if os.path.exists(symlink_fn):
            if not os.path.islink(symlink_fn):
                raise Exception(
                    f"Cannot prepare {reference_dir} because it contains {symlink_fn} "
                    + "which is not a symlink."
                )
            os.unlink(symlink_fn)
        os.symlink(reference_dir, symlink_fn)
