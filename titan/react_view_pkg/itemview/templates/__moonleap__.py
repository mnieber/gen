from moonleap.utils.fp import uniq
from titan.api_pkg.pipeline.resources import PipelineData


def get_helpers(_):
    class Helpers:
        item_view = _.component
        type_spec = item_view.item.type_spec
        data = PipelineData()
        pipelines = _.component.pipelines

        def __init__(self):
            self.data.update(self.pipelines)

        @property
        def fields(self):
            result = []

            for field_spec in self.type_spec.get_field_specs():
                if (
                    "client" in field_spec.has_model
                    and field_spec.name not in ("id",)
                    and field_spec.field_type not in ("slug", "fk", "relatedSet")
                ):
                    result.append(field_spec)

            return result

        @property
        def type_specs_to_import(self):
            return uniq(
                [x.type_spec for x in self.data.prop_items]
                + [x.item.type_spec for x in self.data.prop_item_lists]
            )

    return Helpers()
