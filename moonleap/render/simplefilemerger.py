from pathlib import Path

from moonleap.render.merge import FileMerger


class SimpleFileMerger(FileMerger):
    patterns = []

    @classmethod
    def add_patterns(cls, patterns):
        for pattern in patterns:
            if pattern not in cls.patterns:
                cls.patterns.append(pattern)

    def matches(self, fn):
        return Path(fn).name in SimpleFileMerger.patterns

    def merge(self, lhs_content, rhs_content):
        return lhs_content + rhs_content
