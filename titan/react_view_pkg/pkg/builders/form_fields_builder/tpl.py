from moonleap import Tpls, chop0

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
    {{ form_fields_block }}
    <SaveButton
      label="Save"
      disabled={false}
    />
    """
)

form_field_tpl = chop0(
    """
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
  """
)

tpls = Tpls(
    "form_fields_builder",
    form_fields_tpl=form_fields_tpl,
    form_field_tpl=form_field_tpl,
    form_fields_imports_tpl=form_fields_imports_tpl,
)
