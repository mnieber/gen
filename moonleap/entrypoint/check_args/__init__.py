def check_args(parser, args):
    if args.smart and args.action != "gen":
        parser.error("You can only use --smart with the 'gen' action")

    if args.sudo and args.action != "diff":
        parser.error("You can only use --sudo with the 'diff' action")

    if args.no_scan and not args.smart:
        parser.error("The --no-scan flag requires --smart")
