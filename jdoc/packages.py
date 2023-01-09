import typing as T
from dataclasses import dataclass, field

from jdoc.scenario import *

if T.TYPE_CHECKING:
    from jdoc.relations import Forwards, Relation


@dataclass
class Rule(Entity):
    pattern: str = field(init=False, default="")


snippet_rule_project_uses_docker_compose = """
@rule("project", uses, "docker-compose)
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
"""


class RuleProjectUsesDockerCompose(Rule):
    pattern: str = "@rule('project', uses, 'docker-compose')"

    def run(self, rel: "Relation", forwards: "Forwards"):
        project, docker_compose = rel.subj_res, rel.obj_res

        infos = [
            f"Note that the rule has access to the project resource and the "
            + f"docker-compose resource. It can enrich these resources with "
            + f"additional information however it likes. Here, we only add "
            + f"a step to the render-cascade so that the docker-compose file "
            + f"is rendered in the project directory."
        ]

        # Here, we fake the addition to the :render-cascade
        project.renders(docker_compose)

        return infos


snippet_rule_created_project = """
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
"""


class RuleCreatedProject(Rule):
    pattern: str = "@rule('project')"

    def run(self, rel: "Relation", forwards: "Forwards"):
        from jdoc.relations import create_relation
        from jdoc.resources import global_root_resource

        project = rel.subj_res
        infos = []

        infos += [
            f"A rule may add to the :render-cascade. Here, the rule stipulates "
            + f"that the project is rendered by the root resource."
        ]

        # Here, we fake the addition to the render-cascade.
        global_root_resource.renders(project)

        infos += [
            f"A rule may return a list of :forwards. These are relations "
            + f"that result from the processed relation. The forwarded "
            + f"relations are processed as if they existed in the same "
            + f"block as the processed relation. Here, the forwarded relation "
            + f"stipulates that the project has a README file."
        ]

        forwards.relations = [create_relation("foo:project", "/has", "readme:file")]

        return infos


class RuleDockerComposeRunsService(Rule):
    pattern: str = "@rule('docker-compose', runs, 'service')"

    def run(self, rel: "Relation", forwards: "Forwards"):
        infos = []
        return infos


snippet_service_runs_tool = """
base_tags = [
    ("pip-compile", ["tool"])
]

@rule('service', runs, 'tool')
def service_runs_tool(service, tool):
    pass

@extend(Service)
class ExtendService:
    tools = P.children(runs, 'tool')
"""


class RuleServiceRunsTool(Rule):
    pattern: str = "@rule('service', runs, 'tool')"

    def run(self, rel: "Relation", forwards: "Forwards"):
        infos = [
            f"This rule captures all cases where a service runs a tool. "
            + f"The pip-compile resource is a tool because it was created "
            + f"from the term ':pip-compile' and it was stipulated - in "
            + f"base_tags - that this term has 'tool' as its base_tag."
        ]

        infos += [
            f"In the snippet, we see that the Service class is extended "
            f"so that it gives access to all the tools that it is related to."
        ]

        return infos


@dataclass
class Package(Entity):
    name: str = field(init=False)
    rules: T.List[Rule] = field(default_factory=list)


class DefaultPackage(Package):
    def __post_init__(self):
        self.name = "default-package"

    def install(self):
        infos = [
            "When a package is installed, then Moonleap will automatically "
            "find all rules in the package."
        ]

        self.rules = [
            Rule(pattern="@create('project'"),
            RuleCreatedProject(),
            Rule(pattern="@create('service'"),
            Rule(pattern="@create('docker-compose'"),
            RuleProjectUsesDockerCompose(),
            RuleDockerComposeRunsService(),
        ]

        return infos


class DjangoPackage(Package):
    def __post_init__(self):
        self.name = "django-package"

    def install(self):
        self.rules = [RuleServiceRunsTool()]
