from moonleap.entrypoint import create_session, diff, gen, get_spec_fn, parse_args
from moonleap.entrypoint.check_args import check_args

# import traceback

if __name__ == "__main__":
    args = parse_args()
    smart = args.smart or args.smart_with_skip
    check_args(args, smart)

    session = create_session(args)
    spec_fn = get_spec_fn(args)

    if args.action == "gen":
        try:
            gen(args, smart, session, spec_fn)
        # except Exception as e:
        #     report("Error: " + str(e))
        #     if args.stacktrace:
        #         traceback.print_exc()
        finally:
            pass

    if args.action == "diff":
        diff(session, args.sudo)
