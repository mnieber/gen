import React from 'react';

import {
  useFormStateContext,
  createFormFieldProps,
} from 'react-form-state-context';
import { useFormFieldContext } from 'src/forms/components/FormFieldContext';

// Generic component that shows a text input initialized with the value
// for `fieldName` in the current form state.
export const TextField: React.FC<any> = ({
  controlled,
  ...otherProps
}: any) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  return (
    <input
      {...otherProps}
      type="text"
      {...createFormFieldProps({
        formState,
        controlled,
        fieldName: fieldContext.fieldName,
        fieldType: 'text',
        onChange: otherProps.onChange,
      })}
    />
  );
};
