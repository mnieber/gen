def module_path(self):
    return self.merged_output_path.relative_to(self.module.service.merged_output_path)
