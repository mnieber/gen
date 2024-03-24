def parse_args(parser):
    parser.add_argument("--spec", required=True, dest="spec_dir")
    parser.add_argument(
        "--ask",
        required=False,
        action="store_true",
        help="Ask to create directories",
    )
    parser.add_argument("--output-dir", required=False, default=".moonleap")
    parser.add_argument("--stacktrace", required=False, action="store_true")
    parser.add_argument("action", choices=["gen"])

    return parser.parse_args()
