class ItemHelper:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self._named_item = None
        self._working_item_name = None
        self._has_data = False

    @property
    def named_item(self):
        if not self._has_data:
            self._get_data()

        return self._named_item

    @property
    def working_item_name(self):
        if not self._has_data:
            self._get_data()

        return self._working_item_name

    def _get_data(self):
        self._has_data = True
        if pipeline := self.widget_spec.get_pipeline_by_name("item", recurse=True):
            self._named_item = pipeline.resources[-1]
            self._working_item_name = self._named_item.meta.term.data

    def item_data_path(self):
        if pipeline := self.widget_spec.get_pipeline_by_name("item", recurse=True):
            named_item = pipeline.resources[-1]
            return pipeline.get_data_path(obj=named_item)
        return None
