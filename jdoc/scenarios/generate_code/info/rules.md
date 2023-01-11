# Rules

## @rule('project', uses, 'docker-compose')

```python
@rule("project", uses, "docker-compose")
def project_uses_docker_compose(project, docker_compose):
    project.renders(
        [docker_compose],
        # Render in the project directory
        ".",
        # Extend the rendering context with the docker_compose resource
        dict(docker_compose=docker_compose),
        # This is the path to the templates directory
        [Path(__file__).parent / "templates"],
    )
```

Note that the rule has access to the project resource and the docker-compose resource.
It can enrich these resources with additional information however it likes. Here, we
only add a step to the render-cascade so that the docker-compose file is rendered in
the project directory.

## @rule('project')

```python
@rule("project")
def created_project(project):
    get_root_resource().renders(
        [project],
        "src",
        dict(project=project),
        [Path(__file__).parent / "templates"],
    )

    return [
        create_forward(project, has, "readme:file")
    ]
```

`Adding to the :render-cascade`

A rule may add to the :render-cascade. Here, the rule stipulates that the project is
rendered by the root resource.

`Returning :forwards`

A rule may return a list of :forwards. These are relations that result from the processed
relation. The forwarded relations are processed as if they existed in the same block as
the processed relation. Here, the forwarded relation stipulates that the project has a
README file.

## The react_modules_have_components rule

The {react_modules_have_components_rule.t} iterates over all the :widget-specs in the
{global_widget_reg.t}. For every :widget-spec it creates forward relations that
stipulate that a particular react-module defines the component.

## The create_pipelines_for_component rule

The {create_pipelines_for_component.t} runs for every component that is created. It creates the :pipelines
for this component. To add the :pipelines to the component, it returns new
forward relations of the form ('component', has, 'pipeline').

## The service_runs_tool rule

```python
base_tags = [
    ("pip-compile", ["tool"])
]

@rule('service', runs, 'tool')
def service_runs_tool(service, tool):
    pass

@extend(Service)
class ExtendService:
    tools = P.children(runs, 'tool')
```

`The 'tool' base_tag`

This rule captures all cases where a service runs a tool. The pip-compile resource
is a tool because it was created from the term ':pip-compile' and it was
stipulated - in base_tags - that this term has 'tool' as its base_tag.

`Extending the Service class`

In the snippet, we see that the Service class is extended so that it gives access
to all the tools that it is related to.
