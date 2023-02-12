def parse_args(parser):
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
        "--no-scan",
        required=False,
        action="store_true",
        help="If true, then the --smart option is made a little faster by not "
        + "scanning the output directory and creating symlinks to expected files.",
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
