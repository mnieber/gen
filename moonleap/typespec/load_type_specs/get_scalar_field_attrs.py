from moonleap.utils.pop import pop


def get_scalar_field_attrs(key):
    field_attrs = dict(field_type=None, default_value=None, choices=None)

    #
    # derived
    #
    key, field_attrs["derived"] = pop(key, "^")

    #
    # required
    #
    key, optional = pop(key, "?")
    field_attrs["required"] = not optional

    #
    # api
    #
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

        field_attrs["api"] = (
            ["server"]
            if server_api
            else ["client"]
            if client_api
            else []
            if no_api
            else ["server", "client"]
        )

    #
    # name
    #
    field_attrs["name"] = key.strip()

    return key, field_attrs
