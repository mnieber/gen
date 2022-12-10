from moonleap import Tpls, chop0

form_fields_imports_tpl = chop0(
    """
{% magic_with __.mutation.name as postMyMutation %}
import * as R from 'ramda';
import {
  FormStateProvider,
  HandleValidateArgsT,
  HandleSubmitArgsT,
  unflatten
} from 'react-form-state-context';
import { usePostMyMutation } from 'src/api/mutations';
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
{% end_magic_with %}
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

form_fields_hooks_tpl = chop0(
    """
{% magic_with __.mutation.name as postMyMutation %}
  const postMyMutation = usePostMyMutation().mutateAsync;
  {{ "" }}
{% end_magic_with %}
  """
)

form_fields_preamble_tpl = chop0(
    """
{% magic_with __.mutation.name as postMyMutation %}
    const initialValues = {
      '{{ name }}': {{ __.initial_value(field_spec) }},                                                 {% !! name, field_spec in __.fields %}
    };
    const initialErrors = {};
    const handleValidate = ({values, setError} : HandleValidateArgsT) => {
      if (R.isNil(values['{{ name }}'])) {                                                              {% for name, field_spec in __.validated_fields %}
        setError('{{ name }}', 'This field is required');
      }                                                                                                 {% endfor %}
    };
    const handleSubmit = ({ formState, values }: HandleSubmitArgsT) => {
      return postMyMutation(unflatten(
        {                                                                                               {% if __.uuid_fields %}
          ...values,
          '{{ name }}': values['{{ name }}'].id,                                                        {% !! name, field_spec in __.uuid_fields %}
        }
        values                                                                                          {% else %}{% endif %}
      )).then(() => formState.reset(initialValues, initialErrors));
    };
    {{ ""}}
{% end_magic_with %}
  """
)

tpls = Tpls(
    "form_fields_builder",
    form_fields_preamble_tpl=form_fields_preamble_tpl,
    form_fields_tpl=form_fields_tpl,
    form_field_tpl=form_field_tpl,
    form_fields_hooks_tpl=form_fields_hooks_tpl,
    form_fields_imports_tpl=form_fields_imports_tpl,
)
