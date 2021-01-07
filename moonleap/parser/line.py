from moonleap.parser.term import words_to_terms


class Line:
    def __init__(self, text, words, terms, it_term, block=None):
        self.text = text
        self.words = words
        self.terms = terms
        self.it_term = it_term

    def find_terms_with_tag(self, tag, left_of=None):
        result = []
        for x in self.terms:
            if x.tag == tag:
                result.append(x)
            if left_of and x is left_of:
                break
        return result

    def __str__(self):
        return f"Line: " + ",".join(str(x) for x in self.terms)


def get_create_line():
    def create_line(text, it_term=None):
        terms = []
        words = text.split()
        next_it_term = None
        for term in words_to_terms(words):
            # check if :it must be replaced with it_term
            if term.tag.lower() in ["it", "its"]:
                if not it_term:
                    raise Exception(
                        f":It tag does not refer to a previous resource. Text:\n{text}"
                    )
                terms.append(it_term)
                next_it_term = it_term
            else:
                terms.append(term)
                if not next_it_term:
                    next_it_term = term

        return Line(text, words, terms, next_it_term)

    return create_line
