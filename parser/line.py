class Line:
    def __init__(self, text, terms, it=None):
        self.text = text
        self.terms = terms
        self.it = it

    def find_term_left_of(self, term, tag):
        for x in self.terms:
            if x.tag == tag:
                return x
            if x is term:
                break
        if self.it and self.it.tag == tag:
            return self.it
        return None

    def next_it(self, ittable_lut):
        for term in self.terms:
            if term.tag.lower() in ["it", "its"]:
                return self.it
            if ittable_lut.get(term.tag, False):
                return term
        return None

    def __str__(self):
        return f"Line: " + ",".join(str(x) for x in self.terms)
