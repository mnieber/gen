import React from 'react';
import { useFormStateContext } from 'react-form-state-context';

interface PropsT {
  label: string;
  disabled?: boolean;
  className?: any;
}

export const SaveButton: React.FC<PropsT> = (props: PropsT) => {
  const formState = useFormStateContext();
  return (
    <button
      className={props.className ?? 'ml-2'}
      onClick={(e) => {
        e.preventDefault();
        formState.submit();
      }}
      disabled={props.disabled}
    >
      {props.label}
    </button>
  );
};
