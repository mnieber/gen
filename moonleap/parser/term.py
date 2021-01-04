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


def word_to_term(word):
    parts = word.split(":")
    if len(parts) == 2:
        data, tag = parts
        return Term(data, tag)
    return None


def words_to_terms(words):
    terms = []
    for word in words:
        term = word_to_term(word)
        if term:
            terms.append(term)
    return terms
