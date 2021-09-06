import ramda as R


def tweak(service):
    port = service.get_tweak_or(None, "port")
    if port:
        service.port = port
