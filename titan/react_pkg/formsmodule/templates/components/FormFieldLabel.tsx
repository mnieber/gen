import { isEmpty, isNil } from 'ramda';
import React from 'react';
import { useFormFieldContext } from '/src/forms/components';
import { cn } from '/src/utils/classnames';

type PropsT = React.PropsWithChildren<{
  classNames?: any;
  buttons?: any[];
}>;

export const FormFieldLabel = (props: PropsT) => {
  const fieldContext = useFormFieldContext();

  const ColWrapper =
    isNil(props.children) || isEmpty(props.children)
      ? React.Fragment
      : ({ children }: any) => (
          <div className={cn('FormFieldLabel', 'flex flex-col')}>
            {children}
          </div>
        );

  const RowWrapper =
    isNil(props.buttons) || isEmpty(props.buttons)
      ? ({ children }: any) => <React.Fragment>{children}</React.Fragment>
      : ({ children }: any) => (
          <div
            className={cn(
              'FormFieldLabel__Children',
              'flex flex-row items-center'
            )}
          >
            {children}
          </div>
        );

  return (
    <ColWrapper>
      <RowWrapper>
        {fieldContext.label && (
          <label
            className={cn('FormFieldLabel font-bold', props.classNames)}
            htmlFor={fieldContext.fieldName}
          >
            {fieldContext.label}
          </label>
        )}
        {props.buttons?.length && <div className="flex-grow" />}
        {props.buttons?.length && (
          <div
            className={cn('FormFieldLabel__Buttons', 'flex flex-row', 'ml-2')}
          >
            {props.buttons}
          </div>
        )}
      </RowWrapper>
      {props.children}
    </ColWrapper>
  );
};
