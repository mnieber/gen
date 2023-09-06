def get_helpers(_):
    class Helpers:
        @property
        def item_source(self):
            if _.container.display_bvr:
                return _.container.display_bvr.facet_name
            if _.container.store_bvr:
                return _.container.store_bvr.facet_name
            return None

    return Helpers()
