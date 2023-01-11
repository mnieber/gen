expanded_markdown = """
    # The todo-app:project

    The todo-app:project /uses a :docker-compose file that /runs the backend:service.

    ## The frontend:service {frontend:service}

    The frontend:service /has a :react-app.
"""

widget_spec_todos_yaml = """
todo-:view as Div:
    todo-form-:view: pass

todo-form-:view as Div:
  __attrs__: item=+todo:item
  FormStateProvider:
    __attrs__: fields=name,description
"""
