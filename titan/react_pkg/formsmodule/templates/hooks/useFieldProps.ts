import {
  createFormFieldProps,
  FormState,
  useFormStateContext,
} from 'react-form-state-context';
import {
  FormFieldContextPropsT,
  useFormFieldContext,
} from 'src/forms/components';
import { handleEnterAsTabToNext } from 'src/forms/utils';

type FieldTypeT = 'checkbox' | 'text' | 'password';

export type FieldPropsT = {
  fieldType: FieldTypeT;
  placeholder?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  controlled?: boolean;
};

export const useFieldProps = (props: FieldPropsT) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  return {
    ...createFormFieldProps({
      formState,
      fieldName: fieldContext.fieldName,
      fieldType: props.fieldType,
      onChange: props.onChange,
      controlled: props.controlled,
    }),
    onKeyDown: handleKeyDown(fieldContext, formState),
    placeholder:
      props.placeholder ??
      (fieldContext.useSmartLabel ? fieldContext.label : undefined),
    autoFocus: fieldContext.autoFocus,
  };
};

export function handleKeyDown(
  fieldContext: FormFieldContextPropsT,
  formState: FormState
) {
  return (e: any) => {
    if (fieldContext.submitOnEnter && e.keyCode === 13) {
      formState.submit();
    } else if (fieldContext.tabOnEnter ?? true) {
      handleEnterAsTabToNext(e);
    }
  };
}
