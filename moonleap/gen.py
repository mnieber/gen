import os
import sys
import traceback

import leap_mn
import mistune

from moonleap import config, create_resources, parser

leap_mn.install_all()


def main(gen_file):
    with open(gen_file) as ifs:
        raw_markdown = ifs.read()

    blocks = parser.get_blocks(raw_markdown)
    create_resources(blocks)

    for block in blocks:
        print(block.describe())


def report(x):
    print(x)


if __name__ == "__main__":
    gen_file = "genspec.md"
    if not os.path.exists(gen_file):
        report("Genspec file not found: " + gen_file)
        sys.exit(1)

    try:
        main(gen_file)
    except Exception as e:
        report(f"Error: {e}")
        report(traceback.format_exc(e))
