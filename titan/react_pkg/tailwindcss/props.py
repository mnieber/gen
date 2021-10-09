def has_tailwind_css(self):
    return [x for x in self.service.tools if x.name == "tailwind_css"]
