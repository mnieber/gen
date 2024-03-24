def check_args(parser, args):
    if args.ask and args.action != "gen":
        parser.error("You can only use --ask with the 'gen' action")
