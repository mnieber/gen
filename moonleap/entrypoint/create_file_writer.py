from moonleap.render.file_writer import FileWriter


def create_file_writer(session, args):
    file_writer = FileWriter(
        session.snapshot_fn,
        check_crc_before_write=args.smart or args.smart_with_skip,
        restore_missing_files=args.restore_missing_files,
    )
    return file_writer
