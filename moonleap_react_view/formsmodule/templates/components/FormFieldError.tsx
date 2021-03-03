import classNames from 'classnames';
import React from 'react';

import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from 'src/forms/components/FormFieldContext';

interface IProps {
  extraClass?: string;
  extraClassOnError?: string;
}

// Generic component that shows the error in fieldName for the current
// form state.
export const FormFieldError: React.FC<IProps> = ({
  extraClass,
  extraClassOnError,
}) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();

  const error = formState.getError(fieldContext.fieldName);

  return (
    <p
      className={classNames(
        'text-sm text-red-400',
        extraClass,
        extraClassOnError
          ? {
              extraClassOnError: !!error,
            }
          : {}
      )}
    >
      {error}
    </p>
  );
};
