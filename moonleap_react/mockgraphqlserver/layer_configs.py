from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(aliases={"serve-mocks": "exec sh /app/src/mockServer/start.sh"}),
        )

    return LayerConfig(lambda x: inner())


def get_for_project(service_name):
    def inner():
        return dict(
            MENU=dict(
                #
                commands=dict(
                    #
                    serve=[f"dodo {service_name}.serve-mocks"]
                )
            ),
        )

    return LayerConfig(lambda x: inner())
