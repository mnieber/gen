from moonleap.utils.case import u0
from moonleap.utils.inflect import plural


def magic_replace(text, magic_real_pairs):
    result = text
    for magic_word, real_word in magic_real_pairs:
        real_words = plural(real_word)
        result = (
            result.replace(u0(magic_word) + "s", u0(real_words))
            .replace(u0(magic_word), u0(real_word))
            .replace(magic_word + "s", real_words)
            .replace(magic_word, real_word)
        )
    return result
