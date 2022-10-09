from moonleap.utils.fp import add_to_list_as_set
from moonleap.utils.pop import pop


def strip_generic_symbols(key):
    parts = list()
    key = key.replace("_", "")

    key, derived = pop(key, "^")
    if derived:
        add_to_list_as_set(parts, "derived")

    key, optional = pop(key, "?")
    if optional:
        add_to_list_as_set(parts, "optional")

    if True:
        key, server_api = pop(key, "/")
        key, client_api = pop(key, "\\")
        key, no_api = pop(key, "|")

        if server_api and client_api:
            raise Exception(
                f"Bad key: {key}. Instead of specifying both server and "
                + "client API, just leave it blank"
            )

        if (server_api or client_api) and no_api:
            raise Exception(
                f"Bad key: {key}. Cannot have both server/client API and no API"
            )

        if server_api:
            parts.append("server_api")

        if client_api:
            parts.append("client_api")

        if no_api:
            parts.append("no_api")

    return key.strip(), parts
