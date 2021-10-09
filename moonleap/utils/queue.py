next_default_value = "Queue__next_default_value"


class Queue(list):
    def __init__(self, get_skip_token, items=None):
        self.skip_tokens = []
        self.get_skip_token = get_skip_token
        if items:
            self.extend(items)

    def pop(self, pos=None, default_value=None):
        while len(self):
            result = super(Queue, self).pop(pos)
            skip_token = self.get_skip_token(result)
            skipped = skip_token in self.skip_tokens
            if not skipped:
                self.skip_tokens.append(skip_token)
                return result

        return default_value

    def __iter__(self):
        return self

    def __next__(self):
        if len(self) == 0:
            raise StopIteration
        value = self.pop(0, default_value=next_default_value)
        if value == next_default_value:
            raise StopIteration
        return value
