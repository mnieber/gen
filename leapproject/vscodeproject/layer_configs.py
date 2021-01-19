def get(project):
    return dict(
        ROOT=dict(
            aliases=dict(
                code=f"exec -- code $HOME/sublime-projects/{project.name}.code-workspace"
            )
        )
    )
