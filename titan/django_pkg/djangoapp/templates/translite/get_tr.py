from .get_translate import get_translate


def get_tr(source, options):
    tr = get_translate(source, options)

    c = {}  # noqa

    def wrapped(id):
        return eval('f"' + tr(id) + '"')

    return [c, wrapped]
