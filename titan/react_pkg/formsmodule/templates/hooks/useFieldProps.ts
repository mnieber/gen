import React from 'react';
import {
  createFormFieldProps,
  FormState,
  useFormStateContext,
} from 'react-form-state-context';
import {
  FormFieldContextPropsT,
  useFormFieldContext,
} from '/src/forms/components';
import { handleEnterAsTabToNext } from '/src/forms/utils';

type FieldTypeT = 'checkbox' | 'text' | 'password';

export type FieldPropsT = {
  controlled?: boolean;
  disabled?: boolean;
  fieldType: FieldTypeT;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onFocus?: (e: React.FocusEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
  placeholder?: string;
  autoSelect?: boolean;
  tabIndex?: number;
};

export const useFieldProps = (props: FieldPropsT) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  return {
    onFocus: (e: React.FocusEvent<HTMLInputElement>) => {
      if (props.autoSelect) {
        e.target.select();
      }
      props.onFocus && props.onFocus(e);
    },
    onBlur: props.onBlur,
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
    disabled: props.disabled,
    tabIndex: props.tabIndex,
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
