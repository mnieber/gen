import { observer } from 'mobx-react-lite';
import React from 'react';
import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from '/src/forms/components';
import { cn } from '/src/utils/classnames';

// Import styles
import './FormFieldError.scss';

export type PropsT = {
  extraClass?: string;
  extraClassOnError?: string;
};

// Generic component that shows the error in fieldName for the current
// form state.
export const FormFieldError = observer(
  ({ extraClass, extraClassOnError }: PropsT) => {
    const formState = useFormStateContext();
    const fieldContext = useFormFieldContext();

    const error = formState.getError(fieldContext.fieldName);

    return (
      <div
        className={cn(
          'FormFieldError',
          'place-self-center',
          'mt-[-8px]',
          extraClass,
          extraClassOnError
            ? {
                extraClassOnError: !!error,
              }
            : {}
        )}
      >
        {error}
      </div>
    );
  }
);
