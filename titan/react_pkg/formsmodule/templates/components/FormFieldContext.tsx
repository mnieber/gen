import React from 'react';

export type FormFieldContextPropsT = React.PropsWithChildren<{
  fieldName: string;
  label?: string;
  useSmartLabel?: boolean;
  submitOnEnter?: boolean;
  tabOnEnter?: boolean;
  autoFocus?: boolean;
}>;

const getNullFormFieldContext = (): FormFieldContextPropsT => {
  return {
    fieldName: '',
    label: undefined,
    useSmartLabel: false,
    submitOnEnter: false,
    tabOnEnter: false,
    autoFocus: false,
  };
};

const Context = React.createContext(getNullFormFieldContext());

export const FormFieldContext = (
  props: React.PropsWithChildren<FormFieldContextPropsT>
) => {
  const { children, ...contextProps } = props;

  return <Context.Provider value={contextProps}>{children}</Context.Provider>;
};

export const useFormFieldContext = (): FormFieldContextPropsT => {
  return React.useContext(Context);
};
