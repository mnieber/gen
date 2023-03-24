def check_args(parser, args):
    if args.smart and args.action != "gen":
        parser.error("You can only use --smart with the 'gen' action")
