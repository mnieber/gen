import os
import parser
import sys

import mistune

import resources
from config import config

resource_builders = {
    "project": resources.project.Builder,
    "src-dir": resources.srcdir.Builder,
    "git-repository": resources.gitrepository.Builder,
    "layer-group": resources.layergroup.Builder,
    "layer": resources.layer.Builder,
    "pip-compile": resources.pipcompile.Builder,
    "dockerfile": resources.docker_file.Builder,
    "makefile": resources.makefile.Builder,
}


def create_line(text, it=None):
    terms = []
    tags = list(resource_builders.keys())

    for word in text.split():
        parts = word.split(":")
        if len(parts) == 2:
            data, tag = parts
            if tag in tags:
                terms.append(parser.Term(data, tag))
    return parser.Line(text, terms, it)


ittable_lut = {
    "makefile": True,
    "layer-group": True,
    "service": True,
}


is_global_lut = {
    "git-repository": True,
    "layer-group": True,
    "src-dir": True,
    "project": True,
}


def get_blocks(raw_markdown):
    blockCollector = parser.BlockCollector(ittable_lut, create_line)
    mistune.Markdown(renderer=blockCollector)(raw_markdown)
    return blockCollector.blocks


def main(gen_file):
    __import__("pudb").set_trace()
    with open(gen_file) as ifs:
        raw_markdown = ifs.read()

    blocks = get_blocks(raw_markdown)
    parser.extract_resources(
        config.global_block, is_global_lut.keys(), blocks, resource_builders
    )

    print(config.global_block.describe())
    for block in blocks:
        print(block.describe())


def report(x):
    print(x)


if __name__ == "__main__":
    gen_file = "genspec.md"
    if not os.path.exists(gen_file):
        report("Genspec file not found: " + gen_file)
        sys.exit(1)
    main(gen_file)
