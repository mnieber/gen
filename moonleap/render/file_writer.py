from __future__ import unicode_literals

import json
import zlib
from pathlib import Path

from moonleap.render.merge import get_file_merger
from moonleap.session import get_session


class FileWriter:
    def __init__(self, snapshot_fn, check_crc_before_write, restore_missing_files):
        self.output_filenames = []
        self.warnings = []
        self.root_dir = Path(get_session().output_root_dir)
        self.check_crc_before_write = check_crc_before_write
        self.restore_missing_files = restore_missing_files
        self.fn_parts = {}

        self.snapshot_fn = Path(snapshot_fn)
        if self.snapshot_fn.exists():
            with open(snapshot_fn, "r") as f:
                f_str = f.read()
                self.crc_by_fn = json.loads(f_str)
        else:
            self.crc_by_fn = {}

    def write_file(self, fn, content, is_dir=False):
        fn = (self.root_dir / fn).absolute()

        if is_dir:
            fn.mkdir(parents=True, exist_ok=True)
            return

        if get_file_merger(fn):
            self.fn_parts.setdefault(str(fn), []).append(content)
        else:
            self._write(fn, content)

    def _write(self, fn, content):
        fn_str = str(fn)

        if fn_str in self.output_filenames:
            self.warnings.append(f"Warning: writing twice to {fn_str}")

        crc = zlib.crc32(bytes(str.encode(content)))
        if (
            fn_str in self.crc_by_fn
            and self.crc_by_fn[fn_str] == crc
            and self.check_crc_before_write
            and (fn.exists() or not self.restore_missing_files)
        ):
            return

        self.output_filenames.append(fn_str)
        self.crc_by_fn[fn_str] = crc
        if fn.is_symlink():
            fn.unlink()
        fn.parent.mkdir(parents=True, exist_ok=True)
        with open(fn, "w") as ofs:
            ofs.write(content)

    def write_merged_files_and_snapshot(self):
        for fn_str, parts in self.fn_parts.items():
            file_merger = get_file_merger(fn_str)
            assert file_merger
            content = ""
            for part in parts:
                content = file_merger.merge(content, part)
            self._write(Path(fn_str), content)

        with open(self.snapshot_fn, "w") as f:
            json.dump(self.crc_by_fn, f)
