def is_dependent_on(self, service_name):
    for service in self.depends_on:
        if service.name == service_name:
            return True
    return False
