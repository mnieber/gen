from moonleap import Tpls, chop0

form_sp_imports_tpl = chop0(
    """
{% magic_with __.mutation.name as postMyMutation %}
import * as R from 'ramda';
import {
  FormStateProvider,
  HandleValidateArgsT,
  HandleSubmitArgsT,
  unflatten
} from 'react-form-state-context';
import { usePostMyMutation } from 'src/api/mutations';              {% ?? __.mutation %}
{% end_magic_with %}
  """
)

form_sp_div_open_tpl = chop0(
    """
    <FormStateProvider
        initialValues={initialValues}
        initialErrors={initialErrors}
        handleValidate={handleValidate}
        handleSubmit={handleSubmit}
    >
    """
)

form_sp_div_close_tpl = chop0(
    """
    </FormStateProvider>
    """
)

form_sp_hooks_tpl = chop0(
    """
{% magic_with __.mutation.name as postMyMutation %}
  const postMyMutation = usePostMyMutation().mutateAsync;                                         {% if __.mutation %}
  {{ "" }}                                                                                        {% endif %}
{% end_magic_with %}
  """
)

form_sp_preamble_tpl = chop0(
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
      return postMyMutation(unflatten(                                                                  {% if __.mutation %}
        {                                                                                               {% if __.uuid_fields %}
          ...values,
          '{{ name }}': values['{{ name }}'].id,                                                        {% !! name, field_spec in __.uuid_fields %}
        }
        values                                                                                          {% else %}{% endif %}
      )).then(() => formState.reset(initialValues, initialErrors));                                     {% endif %}
    };
    {{ ""}}
{% end_magic_with %}
  """
)


tpls = Tpls(
    "form_state_provider_builder",
    form_sp_div_open_tpl=form_sp_div_open_tpl,
    form_sp_div_close_tpl=form_sp_div_close_tpl,
    form_sp_preamble_tpl=form_sp_preamble_tpl,
    form_sp_hooks_tpl=form_sp_hooks_tpl,
    form_sp_imports_tpl=form_sp_imports_tpl,
)
