from dataclasses import dataclass

from moonleap import Term
from moonleap.blocks.term import match_term_to_pattern


@dataclass
class WsPipeline:
    term: Term
    term_data_path: str

    def data_path(self, obj):
        if obj and match_term_to_pattern(self.term, obj.meta.term):
            return self.term_data_path

        return None
