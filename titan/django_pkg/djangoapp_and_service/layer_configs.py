from titan.dodo_pkg.layer import LayerConfig


def get(service_name):
    def inner():
        return dict(
            MENU=dict(
                #
                commands=dict(
                    #
                    serve=[f"dodo {service_name}.serve"]
                )
            ),
        )

    return LayerConfig(lambda x: inner())
