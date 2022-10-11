import typing as T
from dataclasses import dataclass

from .language import get_language


@dataclass
class TranslatorOptions:
    language: T.Optional[str] = None
    mark_broken: T.Optional[bool] = False
    check_sources: T.Optional[bool] = True


class Translator:
    def __init__(self, source, options: TranslatorOptions):
        self.source = source
        self.options = options

    def _translate(self, node, version, result):
        key = (self.options.language or get_language()) + "_" + str(version)
        if not node.get(key):
            return False

        result["translation"] = node[key]
        result["broken_translation"] = (
            "!" + result["translation"] + "!"
            if self.options.mark_broken and self.options.mark_broken == True
            else (
                self.options.mark_broken(result["translation"])
                if self.options.mark_broken and callable(self.options.mark_broken)
                else (
                    "!" + result["translation"] + "!"
                    if self.options.mark_broken
                    else result["translation"]
                )
            )
        )

        return True

    def translate(self, id):
        node = self.source.get(id)
        if not node:
            raise Exception("tr: unknown id: " + id)

        version = node["v"]
        while version >= 0:
            result = {}
            if self._translate(node, version, result):
                return (
                    result["broken_translation"]
                    if version < node["v"]
                    else result["translation"]
                )
            version -= 1

        return "!Unknown language: " + (self.options.language or get_language()) + "!"
