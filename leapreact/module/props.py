def add_component(module, component):
    module.components.append(component)
    module.service.add_tool(component)
    component.output_path = module.output_path
