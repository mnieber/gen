import os
from pathlib import Path


def get_spec_fn(args):
    if not os.path.exists(args.spec_dir):
        raise Exception("Spec directory not found: " + args.spec_dir)

    spec_fn = Path(args.spec_dir) / "spec.md"
    if not spec_fn.exists():
        raise Exception(f"Spec file not found: {spec_fn}")
    return spec_fn
