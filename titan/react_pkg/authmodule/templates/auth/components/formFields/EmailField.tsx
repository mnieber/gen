import {
  useFormStateContext,
  createFormFieldProps,
} from 'react-form-state-context';
import { useFormFieldContext } from 'src/forms/components/FormFieldContext';

type PropsT = {};

export const EmailField = (props: PropsT) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  return (
    <input
      autoFocus
      placeholder={fieldContext.label}
      {...createFormFieldProps({
        formState,
        fieldName: fieldContext.fieldName,
        fieldType: 'text',
      })}
    />
  );
};
