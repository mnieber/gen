import { observer } from 'mobx-react-lite';
import * as R from 'ramda';
import React from 'react';
import { useFormStateContext } from 'react-form-state-context';
import {
  FormFieldContext,
  FormFieldContextPropsT,
  FormFieldError,
  FormFieldLabel,
} from 'src/forms/components';
import { cn } from 'src/utils/classnames';
import './Field.scss';

type PropsT = React.PropsWithChildren<
  FormFieldContextPropsT & {
    buttons?: any[];
    className?: any;
    classNameWithLabel?: any;
  }
>;

export const Field = observer((props: PropsT) => {
  const formState = useFormStateContext();

  const value = formState.values[props.fieldName];
  const hasValue = !R.isNil(value) && !R.isEmpty(value);
  const showSmartLabel = !!(hasValue && props.useSmartLabel);

  return (
    <FormFieldContext {...props}>
      <div
        className={cn(
          'Field',
          'px-6',
          'mb-4',
          'flex flex-col justify-center',
          props.className,
          (showSmartLabel || !props.useSmartLabel) && [
            'pb-1',
            props.classNameWithLabel,
          ]
        )}
      >
        {showSmartLabel && (
          <div className={cn('Field__SmartLabel', 'mt-2')}>{props.label}</div>
        )}
        {!props.useSmartLabel && <FormFieldLabel buttons={props.buttons} />}
        {props.children}
      </div>
      <FormFieldError />
    </FormFieldContext>
  );
});
