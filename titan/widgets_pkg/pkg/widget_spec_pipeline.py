from dataclasses import dataclass

from moonleap import Term
from moonleap.parser.term import match_term_to_pattern


@dataclass
class WsPipeline:
    term: Term
    term_data_path: str

    def data_path(self, obj=None, obj_term=None):
        if obj:
            raise NotImplementedError()

        if obj_term and match_term_to_pattern(self.term, obj_term):
            return self.term_data_path

        return None
