import { observer } from 'mobx-react-lite';
import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from '/src/forms/components';
import { tabToNext } from '/src/forms/utils';
import { cn } from '/src/utils/classnames';
import {
  PickerValueT,
  ValuePicker,
  PropsT as ValuePickerPropsT,
} from '/src/utils/components/ValuePicker';
import { useScheduledCall } from '/src/utils/hooks';

type PropsT<ValueT> = Omit<
  ValuePickerPropsT<ValueT> & {
    submitOnChange?: boolean;
  },
  'pickableValue'
>;

export const ValuePickerField = observer(<ValueT,>(props: PropsT<ValueT>) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();
  const formValue = formState.values[fieldContext.fieldName];
  const scheduleSubmit = useScheduledCall(formState.submit);

  const saveChanges = (value: any, { action }: any) => {
    const toPickableValue = (value: PickerValueT) => {
      return value.value;
    };

    const pickableValue = props.isMulti
      ? (value || []).map(toPickableValue)
      : toPickableValue(value);

    formState.setValue(fieldContext.fieldName, pickableValue);
    if (props.submitOnChange) {
      scheduleSubmit();
    }
  };

  const valuePickerProps = {
    ...props,
    pickableValue: formValue,
  };

  return (
    // @ts-ignore
    <ValuePicker
      {...{
        ...valuePickerProps,
        className: cn('ValuePickerField', [props.className]),
      }}
      name={fieldContext.fieldName}
      placeholder={props.placeholder ?? ''}
      noOptionsMessage={() => '...'}
      loadingMessage={() => 'loading...'}
      onChange={saveChanges}
      onKeyDown={(e: any) => {
        if (e.keyCode === 13 && (props.tabOnEnter ?? true)) {
          e.preventDefault();
          tabToNext(e);
        }
        if (props.onKeyDown) {
          props.onKeyDown(e);
        }
      }}
      styles={customStyles}
    ></ValuePicker>
  );
});

const customStyles = {};
