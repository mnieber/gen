import json
import zlib
from pathlib import Path

from moonleap.render.merge import get_file_merger
from moonleap.session import get_session


class FileWriter:
    def __init__(self, snapshot_fn):
        self._all_output_filenames = []
        self.output_filenames = []
        self.warnings = []
        self.root_dir = Path(get_session().output_root_dir)
        self.check_crc_before_write = True
        self.snapshot_fn = Path(snapshot_fn)
        if self.snapshot_fn.exists():
            with open(snapshot_fn, "r") as f:
                f_str = f.read()
                self.crc_by_fn = json.loads(f_str)
                self.crc_by_fn_memo = json.loads(f_str)
        else:
            self.crc_by_fn = {}
            self.crc_by_fn_memo = {}

    def write_file(self, fn, content, is_dir=False):
        fn = (self.root_dir / fn).resolve()
        if is_dir:
            fn.mkdir(parents=True, exist_ok=True)
            return
        fn.parent.mkdir(parents=True, exist_ok=True)

        if fn in self._all_output_filenames:
            file_merger = get_file_merger(fn)
            if file_merger:
                with open(fn) as ifs:
                    lhs_content = ifs.read()
                    content = file_merger.merge(lhs_content, content)
            else:
                self.warnings.append(f"Warning: writing twice to {fn}")
        else:
            self._all_output_filenames.append(fn)

        crc = zlib.crc32(bytes(str.encode(content)))
        if (
            str(fn) in self.crc_by_fn
            and self.crc_by_fn[str(fn)] == crc
            and self.check_crc_before_write
        ):
            return
        else:
            self.crc_by_fn[str(fn)] = crc

        self.output_filenames.append(fn)
        if fn.islink():
            fn.unlink()
        with open(fn, "w") as ofs:
            ofs.write(content)

        # The same file may get written multiple times if there is a file_merger for it.
        # Therefore, to find out of the file changed compared to its historical version, we need to
        # compare its CRC again, using crc_by_fn_memo as the reference data.
        if (
            str(fn) in self.crc_by_fn_memo
            and self.crc_by_fn_memo[str(fn)] == crc
            and self.check_crc_before_write
        ):
            self.output_filenames.remove(fn)

    def write_snapshot(self):
        with open(self.snapshot_fn, "w") as f:
            json.dump(self.crc_by_fn, f)
