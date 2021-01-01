import os
import sys
import traceback

import leap_mn
import mistune

from moonleap import config, create_resources, parser, render_resources

leap_mn.install_all()


def main(gen_file):
    with open(gen_file) as ifs:
        raw_markdown = ifs.read()

    blocks = parser.get_blocks(raw_markdown)
    create_resources(blocks)

    for block in blocks:
        print(block.describe())

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    render_resources(blocks, output_dir)


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
