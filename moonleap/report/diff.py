import json
import os
import shutil
from pathlib import Path

import ramda as R
from moonleap.utils.crc import crc32
from plumbum import local

snapshot_fn = ".moonleap/snapshot.json"


def _diff_tool(settings):
    return R.path_or("diff", ["bin", "diff_tool"])(settings)


def _diff(session, from_dir, to_dir, sudo=False):
    diff_tool = _diff_tool(session.settings)
    if diff_tool == "meld":
        args = ["meld", from_dir, to_dir]
    else:
        session.report(f"Unknown diff tool: {diff_tool}")
        return

    if sudo:
        args.insert(0, "sudo")
    local[args[0]](*args[1:])


def diff(session, sudo=False):
    _diff(session, ".moonleap/output", session.expected_dir, sudo)


def create_snapshot():
    crc_by_fn = {}
    for fn in Path(".moonleap/output").rglob("*"):
        if not os.path.isdir(fn):
            crc = crc32(fn)
            crc_by_fn[str(fn)] = crc

    with open(snapshot_fn, "w") as f:
        json.dump(crc_by_fn, f)


def smart_diff(session, sudo=False):
    if not os.path.exists(snapshot_fn):
        raise FileNotFoundError(
            f"The snapshot file {snapshot_fn} was not found."
            + "You can create it with the 'snap' command."
        )

    with open(snapshot_fn, "r") as f:
        crc_by_fn = json.load(f)

    smart_diff_dir = "./.moonleap/smart_diff"
    if os.path.exists(smart_diff_dir):
        shutil.rmtree(smart_diff_dir)
    os.mkdir(smart_diff_dir)

    smart_output_dir = Path(smart_diff_dir) / "output"
    smart_ref_dir = Path(smart_diff_dir) / "ref"
    ref_dir = Path(session.expected_dir)

    for fn in Path(".moonleap/output").rglob("*"):

        if not os.path.isdir(fn):
            crc = crc32(fn)
            if crc != crc_by_fn.get(str(fn), ""):
                rel_fn = fn.relative_to(".moonleap/output")

                smart_output_fn = smart_output_dir / rel_fn
                os.makedirs(str(smart_output_fn.parent), exist_ok=True)
                smart_output_fn.symlink_to(fn.absolute())

                ref_fn = ref_dir / rel_fn
                if ref_fn.exists():
                    smart_ref_fn = smart_ref_dir / rel_fn
                    os.makedirs(str(smart_ref_fn.parent), exist_ok=True)
                    smart_ref_fn.symlink_to(ref_fn.absolute())

    _diff(session, smart_output_dir, smart_ref_dir, sudo)
