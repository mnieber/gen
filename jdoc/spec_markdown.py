from dataclasses import dataclass

from jdoc.scenario import *
from jdoc.verbs import *


@dataclass
class RawMarkdown(Entity):
    contents = """
        # The foo:project

        The foo:project /uses a :docker-compose file that /runs the backend:service.

        ## The [backend:service](./backend-service.md)
    """


@dataclass
class ExpandedMarkdown(Entity):
    contents = ""


@dataclass
class ExpandMarkdownFn(Entity):
    def expand_markdown(
        self, raw_markdown: RawMarkdown, expanded_markdown: ExpandedMarkdown
    ):
        """Simulate the expansion of the markdown by replacing the link
        with the contents of the linked file. This also adds a scope name
        to the block heading.
        """
        new_markdown = raw_markdown.contents.replace(
            "## The [backend:service](./backend-service.md)",
            """
            ## The backend:service {backend:service}

            The backend:service /uses :pip-compile.
        """,
        )

        assert new_markdown != raw_markdown.contents
        expanded_markdown.contents = new_markdown
