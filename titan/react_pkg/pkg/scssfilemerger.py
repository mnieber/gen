import os
from pathlib import Path

from moonleap.render.merge import FileMerger


class ScssFileMerger(FileMerger):
    patterns = ["index.scss"]

    @classmethod
    def add_pattern(cls, pattern):
        if pattern not in cls.patterns:
            cls.patterns.append(pattern)

    def matches(self, fn):
        return Path(fn).name in ScssFileMerger.patterns

    def merge(self, lhs_content, rhs_content):
        return lhs_content + rhs_content
