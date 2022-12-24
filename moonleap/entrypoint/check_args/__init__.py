def check_args(args, smart):
    if smart and args.action != "gen":
        raise Exception("You can only use --smart with the 'gen' action")

    if args.restore_missing_files and not smart:
        raise Exception("You can only use --restore-missing together with --smart")

    if args.sudo and args.action != "diff":
        raise Exception("You can only use --sudo with the 'diff' action")
