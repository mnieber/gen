import React from 'react';

import { useFormStateContext } from 'react-form-state-context';

type PropsT = {
  label: string;
  dataCy: string;
};

export const SubmitButton = (props: PropsT) => {
  const formState = useFormStateContext();
  const onClick = () => {
    formState.submit();
  };

  return (
    <button data-cy={props.dataCy} type="submit" className="" onClick={onClick}>
      {props.label}
    </button>
  );
};
