def merge_into_config(config, layer, xpath=None):
    def _is_list(x):
        return isinstance(x, type(list()))

    def _is_dict(x):
        return isinstance(x, type(dict()))

    def _raise(xpath):
        raise Exception(
            "Cannot merge configurations. Check key /%s" % "/".join(new_xpath)
        )

    xpath = xpath or []
    for key, val in (layer or {}).items():
        new_xpath = xpath + [key]

        if _is_dict(val):
            config.setdefault(key, {})
            if not _is_dict(config[key]):
                _raise(new_xpath)
            merge_into_config(config[key], val, new_xpath)
        elif _is_list(val):
            config.setdefault(key, [])
            if not _is_list(config[key]):
                _raise(new_xpath)
            for x in val:
                if x not in config[key]:
                    config[key].append(x)
        else:
            config[key] = val
