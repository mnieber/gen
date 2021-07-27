def module_path(self):
    return self.merged_output_path.relative_to(self.module.react_app.merged_output_path)
