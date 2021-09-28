def wrapped_components(self):
    if self.wrapped_child_components:
        return self.wrapped_child_components

    result = []
    for child_component in self.child_components:
        child_result = wrapped_components(child_component)
        if child_result:
            if result:
                raise Exception(
                    f"The {self.name} component has more than one child component "
                    + r"that wraps its children. This is invalid. Please check the spec file"
                )
            result = child_result

    return result
