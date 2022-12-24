from moonleap.entrypoint import create_session, diff, gen, parse_args
from moonleap.entrypoint.check_args import check_args

# import traceback

if __name__ == "__main__":
    args = parse_args()
    smart = args.smart or args.smart_with_skip
    check_args(args, smart)

    session = create_session(args)

    if args.action == "gen":
        try:
            gen(args, smart, session)
        # except Exception as e:
        #     report("Error: " + str(e))
        #     if args.stacktrace:
        #         traceback.print_exc()
        finally:
            pass

    if args.action == "diff":
        diff(session, args.sudo)
