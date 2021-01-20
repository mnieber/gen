from leapdodo.layer import LayerConfig


def get(project):
    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(
                    code="exec -- code $HOME/sublime-projects/"
                    + f"{project.name}.code-workspace"
                )
            )
        )

    return LayerConfig(lambda x: inner())
