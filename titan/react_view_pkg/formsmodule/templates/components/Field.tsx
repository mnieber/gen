import React from 'react';
import { FormFieldContext } from 'src/forms/components/FormFieldContext';
import { FormFieldError } from 'src/forms/components/FormFieldError';
import { FormFieldLabel } from 'src/forms/components/FormFieldLabel';

interface FieldT {
  fieldName: string;
  label: string;
  buttons?: any[];
}

export const Field: React.FC<FieldT> = ({
  fieldName,
  label,
  buttons,
  children,
}) => {
  return (
    <FormFieldContext fieldName={fieldName} label={label}>
      <div className="Field flex flex-col">
        <FormFieldLabel buttons={buttons} />
        {children}
        <FormFieldError />
      </div>
    </FormFieldContext>
  );
};
