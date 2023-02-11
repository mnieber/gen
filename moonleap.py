import traceback

from moonleap.entrypoint import create_session, diff, gen, parse_args
from moonleap.entrypoint.check_args import check_args


class NeverException(Exception):
    pass


if __name__ == "__main__":
    args = parse_args()
    check_args(args, args.smart)

    session = create_session(args)

    if args.action == "gen":
        try:
            gen(args, args.smart, session)
        except NeverException as e:
            session.report("Error: " + str(e))
            if args.stacktrace:
                traceback.print_exc()
        finally:
            pass

    if args.action == "diff":
        diff(session, args.sudo)
