import React from 'react';
import { isEmpty, isNil } from 'lodash/fp';
import classnames from 'classnames';
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
          <div className="FormFieldLabel flexcol">{children}</div>
        );

  const RowWrapper =
    isNil(props.buttons) || isEmpty(props.buttons)
      ? ({ children }: any) => <React.Fragment>{children}</React.Fragment>
      : ({ children }: any) => (
          <div className="flexrow items-center">{children}</div>
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
        <div className="flexrow">{props.buttons}</div>
      </RowWrapper>
      {props.children}
    </ColWrapper>
  );
};
