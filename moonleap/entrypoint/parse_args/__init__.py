from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--spec", required=True, dest="spec_dir")
    parser.add_argument(
        "--smart",
        required=False,
        action="store_true",
        help="If true, CRCs of output files are recorded, "
        + "and - on subsequent runs - output files are not written if "
        + "they have the same CRC. Moreover, output files are replaced with "
        + " a symlink if they have the same timestamp as the reference file.",
    )
    parser.add_argument(
        "--smart-with-skip",
        required=False,
        action="store_true",
        help="Same as --smart, but also use the settings/diff/skip patterns "
        + "to create symlinks (in the output) to expected files that must be "
        + "skipped in the diff.",
    )
    parser.add_argument(
        "--post-process-all",
        required=False,
        action="store_true",
        dest="post_process_all_files",
        help="If true, post process all output files, not just the ones that were written",
    )
    parser.add_argument("--output-dir", required=False, default=".moonleap")
    parser.add_argument("--sudo", required=False, action="store_true")
    parser.add_argument("--stacktrace", required=False, action="store_true")
    parser.add_argument("action", choices=["gen", "diff"])

    return parser.parse_args()
