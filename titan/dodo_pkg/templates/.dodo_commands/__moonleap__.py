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


def get_contexts(_):
    result = []
    for layer in _.root_resource.project.layers:
        result.append(dict(layer=layer, service=layer.configures_service))
    return result


def get_meta_data_by_fn(_, __):
    return {
        ".dodo-start-env": {"include": _.layer.is_root},
        "config.yaml.j2": {"include": _.layer.is_root},
        "layer.yaml.j2": {
            "include": not _.layer.is_root,
            "name": f"{_.layer.basename}.yaml",
        },
    }
