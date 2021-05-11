from argparse import ArgumentParser
from pathlib import Path

from dodo_commands import CommandError, ConfigArg, Dodo
from dotenv import dotenv_values


def _args():
    parser = ArgumentParser(description="")

    # Add arguments to the parser here

    # Parse the arguments.
    args = Dodo.parse_args(parser, config_args=[])

    args.cwd = Dodo.get("/ROOT/project_dir")

    # Raise an error if something is not right
    if False:
        raise CommandError("Oops")

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    postgres_env_fn = Path(__file__).parent / "scripts/postgres.env"
    pg_values = dotenv_values(postgres_env_fn)

    Dodo.run(
        "env",
        "PGPASSWORD=dev",
        "psql",
        "-U",
        "postgres",
        "-d",
        "postgres",
        "-c",
        "CREATE DATABASE strapi",
    )

    args = _args()
    Dodo.run([], cwd=args.cwd)
