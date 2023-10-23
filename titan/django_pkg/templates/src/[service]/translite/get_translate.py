from .translator import Translator, TranslatorOptions


def get_translate(source, options: TranslatorOptions):
    if not source:
        raise Exception("get_translate: empty translation source")

    if isinstance(source, list):
        sources = source
        source = {}
        for x in sources:
            if options.check_sources:
                for k in x.keys():
                    if k in source:
                        raise Exception("get_translate: duplicate key: " + k)

            source.update(x)

    translator = Translator(source, options)

    def translate(id):
        return translator.translate(id)

    return translate
