_file_mergers = []


class FileMerger:
    def matches(self, fn):
        raise NotImplementedError()

    def merge(self, lhs_content, rhs_content):
        raise NotImplementedError()


def get_file_merger(fn):
    result = [x for x in _file_mergers if x.matches(fn)]
    if len(result) > 1:
        raise Exception(f"More than one file merger for {fn}")

    return result[0] if result else None


def add_file_merger(file_merger):
    _file_mergers.append(file_merger)
