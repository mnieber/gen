import os

from moonleap.render.file_writer import FileWriter
from moonleap.utils.load_yaml import load_yaml


def create_file_writer(session, args):
    file_writer = FileWriter(
        session.snapshot_fn,
        check_crc_before_write=args.smart,
    )
    return file_writer
