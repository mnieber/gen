from moonleap.utils.case import upper0
from moonleap.utils.inflect import plural


def magic_replace(text, magic_real_pairs):
    result = text
    for magic_word, real_word in magic_real_pairs:
        real_words = plural(real_word)
        result = (
            result.replace(upper0(magic_word) + "s", upper0(real_words))
            .replace(upper0(magic_word), upper0(real_word))
            .replace(magic_word + "s", real_words)
            .replace(magic_word, real_word)
        )
    return result
