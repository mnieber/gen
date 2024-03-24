def parse_args(parser):
    parser.add_argument("--spec", required=True, dest="spec_dir")
    parser.add_argument(
        "--smart",
        required=False,
        action="store_true",
        help="If true, CRCs of output files are recorded, "
        + "and - on subsequent runs - output files are not written if "
        + "they have the same CRC.",
    )
    parser.add_argument("--output-dir", required=False, default=".moonleap")
    parser.add_argument("--stacktrace", required=False, action="store_true")
    parser.add_argument("action", choices=["gen"])

    return parser.parse_args()
