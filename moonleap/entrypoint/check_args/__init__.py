def check_args(args, smart):
    if smart and args.action != "gen":
        raise Exception("You can only use --smart with the 'gen' action")

    if args.sudo and args.action != "diff":
        raise Exception("You can only use --sudo with the 'diff' action")
