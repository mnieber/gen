from __future__ import unicode_literals

import json
import shutil
import zlib
from pathlib import Path

from moonleap.render.file_merger import get_file_merger


class FileWriter:
    def __init__(
        self, snapshot_fn, check_crc_before_write, root_dir, ask_to_create_dirs
    ):
        self.output_filenames = []
        self.ask_to_create_dirs = ask_to_create_dirs
        self.all_output_filenames = []
        self.warnings = []
        self.missing_dirs = []
        self.root_dir = Path(root_dir)
        self.check_crc_before_write = check_crc_before_write
        self.fn_parts = {}
        self.snapshot_fn = Path(snapshot_fn)
        self._load_crc_snapshot(snapshot_fn)

    @property
    def crc_by_fn(self) -> dict:
        return self.snapshot["crc_by_fn"]

    @property
    def files_to_post_process(self) -> list:
        return self.snapshot["files_to_post_process"]

    @property
    def ml_filenames_to_copy(self) -> list:
        return self.snapshot["ml_filenames_to_copy"]

    def _load_crc_snapshot(self, snapshot_fn):
        self.snapshot = dict(
            crc_by_fn={},
            files_to_post_process=[],
            ml_filenames_to_copy=[],
        )
        if self.snapshot_fn.exists():
            with open(snapshot_fn, "r") as f:
                f_str = f.read()
                self.snapshot = json.loads(f_str)

    def write_file(self, fn, content, is_dir=False):
        fn = (self.root_dir / fn).absolute()

        if is_dir:
            fn.mkdir(parents=True, exist_ok=True)
            return

        if get_file_merger(fn):
            if _is_binary(content):
                raise Exception(f"Cannot merge binary file: {fn}")
            self.fn_parts.setdefault(str(fn), []).append(content)
        else:
            self._write(fn, content)

    def _write(self, fn, content):
        fn_str = str(fn)
        ml_fn = fn.parent / ".moonleap" / fn.name
        ml_fn_str = str(ml_fn)

        if ml_fn_str in self.all_output_filenames:
            self.warnings.append(f"Warning: writing twice to {ml_fn_str}")
        else:
            self.all_output_filenames.append(ml_fn_str)

        crc = _crc(content)
        if (
            ml_fn_str in self.crc_by_fn
            and self.crc_by_fn[ml_fn_str] == crc
            and self.check_crc_before_write
            and ml_fn.exists()
        ):
            return

        # At this point we know that the file has changed and we need to write it.
        # First we check if we must create the parent directory.

        parent_dir = ml_fn.parent

        # If parent_dir is a subdir of a missing dir that was already created for the
        # user, then we can just create the parent dir.
        if not parent_dir.exists():
            for missing_dir in self.missing_dirs:
                if missing_dir.exists() and parent_dir.is_relative_to(missing_dir):
                    parent_dir.mkdir(parents=True, exist_ok=True)
                    break

        if not parent_dir.exists:
            # Find the root dir that is missing
            missing_dir = parent_dir
            while not missing_dir.parent.exists():
                missing_dir = missing_dir.parent

            # If we already knew that the dir was missing, then either this was already
            # reported on, or we already asked the user if they want to create it.
            if missing_dir in self.missing_dirs:
                return

            self.missing_dirs.append(missing_dir)
            if self.ask_to_create_dirs:
                create_dir = input(f"Create directory '{missing_dir}'? (Y/n): ")
                if create_dir.lower() not in ("y", "yes", ""):
                    return
            else:
                self.warnings.append(f"Skipping the creation of files in {missing_dir}")
                return

            parent_dir.mkdir(parents=True, exist_ok=True)

        # We will always write the shadow file (with .ml in it).
        # We will also write the original file if it doesn't exist and there is no
        # shadow file yet (when the user removes the original file but keeps the shadow file
        # then it indicates that the user doesn't want to use the shadow file in their project).

        self.output_filenames.append(ml_fn_str)
        self.crc_by_fn[ml_fn_str] = crc
        if ml_fn_str not in self.files_to_post_process:
            self.files_to_post_process.append(ml_fn_str)

        write_to_fn = not fn.exists() and not ml_fn.exists()
        with open(ml_fn_str, "wb" if _is_binary(content) else "w") as ofs:
            ofs.write(content)
        if write_to_fn:
            self.ml_filenames_to_copy.append((ml_fn_str, fn_str))

    def write_merged_files(self):
        for fn_str, parts in self.fn_parts.items():
            file_merger = get_file_merger(fn_str)
            assert file_merger
            content = ""
            for part in parts:
                content = file_merger.merge(content, part)
            self._write(Path(fn_str), content)

    def write_snapshot(self, clear_files_to_post_process):
        if clear_files_to_post_process:
            self.snapshot["files_to_post_process"] = []
            self.snapshot["ml_filenames_to_copy"] = []
        with open(self.snapshot_fn, "w") as f:
            json.dump(self.snapshot, f)

    def copy_ml_files(self):
        for ml_fn_str, fn_str in self.ml_filenames_to_copy:
            if not Path(fn_str).exists():
                shutil.copy(ml_fn_str, fn_str)


def _is_binary(content):
    return isinstance(content, bytes)


def _crc(content):
    blob = content if _is_binary(content) else bytes(str.encode(content))
    return zlib.crc32(blob)
