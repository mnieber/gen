class Term:
    def __init__(self, data, tag):
        self.data = data
        self.tag = tag

    def __str__(self):
        return f"Term tag={self.tag} data={self.data}"

    def __hash__(self):
        return hash((self.tag, self.data))

    def __eq__(self, rhs):
        return self.tag == rhs.tag and self.data == rhs.data


def text_to_terms(text):
    terms = []
    for word in text.split():
        parts = word.split(":")
        if len(parts) == 2:
            data, tag = parts
            terms.append(Term(data, tag))
    return terms


always_term = Term("always", "always")
