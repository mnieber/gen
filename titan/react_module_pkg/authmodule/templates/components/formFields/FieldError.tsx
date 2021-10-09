import React from 'react';

import { useFormStateContext } from 'react-form-state-context';

type PropsT = {
  fieldName: string;
};

export const FieldError = (props: PropsT) => {
  const formState = useFormStateContext();
  const error = formState.errors[props.fieldName];
  return error ? <div>{formState.errors[props.fieldName]}</div> : null;
};
