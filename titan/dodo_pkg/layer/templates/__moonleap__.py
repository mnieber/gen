import os


def get_helpers(_):
    class Helpers:
        vscode_project = _.project.vscode_project
        service_layer_group = _.layer.service_layer_group
        shift_layers = (
            [x for x in service_layer_group.layers if x.configures_service]
            if service_layer_group
            else []
        )

        @property
        def vscode_project_fn(self):
            return (
                f"{self.vscode_project.code_workspaces_dir}/{_.project.kebab_name}.code-workspace"
                if self.vscode_project
                else ""
            )

    return Helpers()
