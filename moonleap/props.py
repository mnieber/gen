class Prop:
    def __init__(self, f, parent_resource_type=None, child_resource_type=None):
        self.prop = property(f)
        self.parent_resource_type = parent_resource_type
        self.child_resource_type = child_resource_type


def parents_of_type(resource_type):
    return Prop(
        lambda self: self.parents_of_type(resource_type),
        parent_resource_type=resource_type,
    )


def parent_of_type(resource_type):
    return Prop(
        lambda self: self.parent_of_type(resource_type),
        parent_resource_type=resource_type,
    )


def children_of_type(resource_type):
    return Prop(
        lambda self: self.children_of_type(resource_type),
        child_resource_type=resource_type,
    )


def child_of_type(resource_type):
    return Prop(
        lambda self: self.child_of_type(resource_type),
        child_resource_type=resource_type,
    )
