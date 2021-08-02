from moonleap import kebab_to_camel, kebab_to_snake, tags

from .resources import UsersModule  # noqa


@tags(["users:module"])
def users_module_created(term, block):
    name_camel = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    module = UsersModule(name_snake=name_snake, name_camel=name_camel)
    module.add_template_dir(__file__, "templates")
    module.output_path = module.name_snake
    return module
