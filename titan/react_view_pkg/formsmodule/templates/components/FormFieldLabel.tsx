import classnames from 'classnames';
import { isEmpty, isNil } from 'ramda';
import React from 'react';
import { useFormFieldContext } from 'src/forms/components/FormFieldContext';

type PropsT = React.PropsWithChildren<{
  classNames?: any;
  buttons?: any[];
}>;

export const FormFieldLabel: React.FC<PropsT> = (props: PropsT) => {
  const fieldContext = useFormFieldContext();

  const ColWrapper =
    isNil(props.children) || isEmpty(props.children)
      ? React.Fragment
      : ({ children }: any) => (
          <div className="FormFieldLabel flex flex-col">{children}</div>
        );

  const RowWrapper =
    isNil(props.buttons) || isEmpty(props.buttons)
      ? ({ children }: any) => <React.Fragment>{children}</React.Fragment>
      : ({ children }: any) => (
          <div className="flex flex-row items-center">{children}</div>
        );

  return (
    <ColWrapper>
      <RowWrapper>
        <label
          className={classnames('mt-2 font-bold', props.classNames)}
          htmlFor={fieldContext.fieldName}
        >
          {fieldContext.label}
        </label>
        <div className="flex flex-row">{props.buttons}</div>
      </RowWrapper>
      {props.children}
    </ColWrapper>
  );
};
