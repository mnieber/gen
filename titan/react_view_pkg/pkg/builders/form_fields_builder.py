import ramda as R

from moonleap import u0
from titan.api_pkg.apiregistry import get_api_reg
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg

from .form_fields_builder_tpl import form_field_tpl, form_fields_tpl


class Helper:
    def __init__(self, item_name, mutation_name):
        self.item_name = item_name
        self.type_spec = get_type_reg().get(u0(self.item_name) + "Form")
        self.mutation = get_api_reg().get(mutation_name)
        self.fields = Helper._get_fields(self.mutation)
        self.uuid_fields = [
            x for x in self.fields if x[1].field_type == "uuid" and x[1].target
        ]

    def slug_src(self, field_spec):
        slug_sources = [
            name for name, field_spec in self.fields if field_spec.is_slug_src
        ]
        return R.head(slug_sources) or "Moonleap Todo: slug_src"

    def label(self, name):
        return u0(name.replace(".", " "))

    def display_field_name(self, type_spec):
        return type_spec.display_field.name if type_spec.display_field else "id"

    @staticmethod
    def _get_fields(mutation):
        scalar_field_specs = [
            x for x in mutation.get_inputs() if x.field_type != "form"
        ]
        fields = []
        fields.extend([(x.name, x) for x in scalar_field_specs])
        for form_field_spec in mutation.get_inputs(["form"]):
            fields.extend(
                [
                    (f"{form_field_spec.name}.{x.name}", x)
                    for x in Helper._form_fields(form_field_spec)
                    if not (x.field_type == "uuid" and not x.target)
                ]
            )
        return fields

    @staticmethod
    def _form_fields(form_field_spec):
        return [
            x
            for x in form_field_spec.target_type_spec.get_field_specs()
            if "client" in x.has_model
        ]


class FormFieldsBuilder(Builder):
    def get_spec_extension(self, places):
        if "Field" not in places:
            layout = "Card" if self.get_value_by_name("card") else "Div"
            return {f"Field with {layout}[cn=__]": {"FormField": "pass"}}

    def build(self):
        __import__("pudb").set_trace()  # qq
        __ = self.__ = Helper(
            item_name=self.named_item_term.data,
            mutation_name=self.get_value_by_name("mutation"),
        )
        field_widget_spec = self.widget_spec.find_child_with_place("Field")
        form_fields_block = ""
        for form_field_name, field_spec in __.fields:
            build_output = self._get_field_widget_output(
                form_field_name, field_widget_spec, field_spec
            )
            form_fields_block += self.output.graft(build_output)

        context = dict(__=__, form_fields_block=form_fields_block)
        self.add(
            lines=[self.render_str(form_fields_tpl, context, "form_fields_tpl.j2")]
        )

    def _get_field_widget_output(self, form_field_name, field_widget_spec, field_spec):
        from titan.react_view_pkg.pkg.build import build

        with field_widget_spec.memo():
            field_widget_spec.values["form_field_name"] = form_field_name
            field_widget_spec.values["field_spec"] = field_spec
            field_widget_spec.values["helper"] = self.__
            return build(field_widget_spec)


class FormFieldBuilder(Builder):
    def build(self):
        field_spec = self.get_value_by_name("field_spec")
        context = dict(
            field_spec=field_spec,
            name=self.get_value_by_name("form_field_name"),
            __=self.get_value_by_name("helper"),
        )
        self.add(lines=[self.render_str(form_field_tpl, context, "form_field_tpl.j2")])
