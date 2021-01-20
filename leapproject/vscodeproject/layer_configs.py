from leapdodo.layer import LayerConfig


def get(project):
    def l():
        return dict(
            ROOT=dict(
                aliases=dict(
                    code=f"exec -- code $HOME/sublime-projects/{project.name}.code-workspace"
                )
            )
        )

    return LayerConfig(lambda x: l())
