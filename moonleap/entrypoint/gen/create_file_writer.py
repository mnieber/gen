import os

from moonleap.render.file_writer import FileWriter
from moonleap.report.symlinks import ml_skip_fn
from moonleap.utils.load_yaml import load_yaml


def create_file_writer(session, args):
    skip_list = []
    if os.path.exists(ml_skip_fn):
        skip_list = load_yaml(ml_skip_fn)
    skip_list.extend(session.get_setting_or([], ["gen", "skip"]))

    file_writer = FileWriter(
        session.snapshot_fn,
        check_crc_before_write=args.smart,
        skip_list=skip_list,
    )
    return file_writer
