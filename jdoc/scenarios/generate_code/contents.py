raw_markdown = """
# The todo-app:project

The todo-app:project /uses a :docker-compose file that /runs the backend:service.

## The [backend:service](./backend-service.md)
"""

expanded_markdown = """
    # The todo-app:project

    The todo-app:project /uses a :docker-compose file that /runs the backend:service.

    ## The backend:service {backend:service}

    The backend:service /uses :pip-compile.
"""

render_resources_snippet = """
VERSION.txt.j2:
    name: "VERSION-{{ _.version_nr }}.txt"
    include: {{ _.has_flag("app/useVersioning")|bool }}
"""
