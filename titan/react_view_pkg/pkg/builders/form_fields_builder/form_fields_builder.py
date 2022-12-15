import os

from moonleap import Tpls, chop0
from titan.react_view_pkg.pkg.builder import Builder

from .helper import Helper


class FormFieldsBuilder(Builder):
    def get_spec_extension(self, places):
        if "Field" not in places:
            return {f"Field with FormField": "pass"}

    def build(self):
        from titan.react_view_pkg.pkg.get_named_data_term import get_named_item_term

        __ = self.__ = Helper(
            item_name=get_named_item_term(self.widget_spec).data,
            mutation_name=self.widget_spec.get_value_by_name("mutation"),
        )
        field_widget_spec = self.widget_spec.find_child_with_place("Field")
        lines = []
        for form_field_name, field_spec in __.fields:
            build_output = self._get_field_widget_output(
                form_field_name, field_widget_spec, field_spec
            )
            lines.extend(build_output.lines)
            self.output.graft(build_output)

        context = dict(__=__, __form_fields_block=os.linesep.join(lines))
        self.add(
            imports_lines=[tpls.render("form_fields_imports_tpl", context)],
            lines=[tpls.render("form_fields_tpl", context)],
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
        field_spec = self.widget_spec.get_value_by_name("field_spec")
        context = dict(
            field_spec=field_spec,
            name=self.widget_spec.get_value_by_name("form_field_name"),
            __=self.widget_spec.get_value_by_name("helper"),
        )
        self.add(lines=[tpls.render("form_field_tpl", context)])


form_fields_imports_tpl = chop0(
    """
import {
  ControlledCheckbox,
  Field,
  GlobalError,
  TextField,
  SaveButton,
  SlugField,
  UpdateSlugButton,
  ValuePickerField
} from 'src/forms/components';
  """
)

form_fields_tpl = chop0(
    """
    <GlobalError />
    {{ __form_fields_block }}
    <SaveButton
      label="Save"
      disabled={false}
    />
    """
)

form_field_tpl = chop0(
    """
{% magic_with field_spec.target as FieldSpecTarget %}
    <Field
      fieldName="{{ name }}"
      label="{{ __.label(name) }}"
      buttons={[                                                                                  {% if field_spec.field_type in ("slug",) %}
        <UpdateSlugButton
          key="1"
          relatedFieldName="{{ __.slug_src(field_spec) }}"
        />
      ]}                                                                                          {% endif %}
    >
      <TextField controlled={true} />                                                             {% ?? field_spec.field_type in ("string", "text", "url") %}
      <SlugField />                                                                               {% ?? field_spec.field_type in ("slug",) %}
      <ValuePickerField                                                                           {% if field_spec.field_type in ("uuid",) and field_spec.target %}
        isCreatable={false}
        isMulti={false}
        pickableValues={props.fieldSpecTargets}
        pickableValue={initialValues['{{ name }}']}
        labelFromValue={(x: any) => x.{{ __.display_field_name(field_spec.target_type_spec) }}}
      />                                                                                          {% endif %}
      <div className="flex flex-row items-begin mt-1"><ControlledCheckbox /></div>                {% ?? field_spec.field_type in ("boolean",) %}
    </Field>
{% end_magic_with %}
  """
)

tpls = Tpls(
    "form_fields_builder",
    form_fields_tpl=form_fields_tpl,
    form_field_tpl=form_field_tpl,
    form_fields_imports_tpl=form_fields_imports_tpl,
)
