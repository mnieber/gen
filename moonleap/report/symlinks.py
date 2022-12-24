from pathlib import Path


def create_symlinks_for_identical_files(session):
    ref_dir = Path(session.expected_dir)
    out_dir = Path(".moonleap/output")

    for fn in out_dir.rglob("*"):
        if fn.is_symlink() and not fn.exists():
            fn.unlink()
        if not fn.is_dir() and not fn.is_symlink():
            ref_fn = (ref_dir / fn.relative_to(out_dir)).absolute()
            if ref_fn.exists() and _same_file(fn.stat(), ref_fn.stat()):
                fn.unlink()
                fn.symlink_to(ref_fn)


def create_symlinks_for_skip_patterns(session):
    ref_dir = Path(session.expected_dir)
    out_dir = Path(".moonleap/output")

    skip = session.get_setting_or([], ["diff", "skip"])
    ref_subdirs = [x.resolve() for x in Path(ref_dir).glob("*")]
    for ref_subdir in ref_subdirs:
        for fn in Path(ref_subdir).rglob("*"):
            prefix = ref_subdir.name + "/"
            p = Path(prefix + str(fn.relative_to(ref_subdir)))

            for skip_pattern in skip:
                if p.match(skip_pattern):
                    out_fn = out_dir / ref_subdir.name / fn.relative_to(ref_subdir)
                    if not out_fn.exists():
                        out_fn.parent.mkdir(parents=True, exist_ok=True)
                        out_fn.symlink_to(fn)


def _same_file(stat_lhs, stat_rhs):
    return (
        stat_lhs.st_mtime == stat_rhs.st_mtime and stat_lhs.st_size == stat_rhs.st_size
    )
