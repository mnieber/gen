import { observer } from 'mobx-react-lite';
import { useFormStateContext } from 'react-form-state-context';
import { useFormFieldContext } from 'src/forms/components/FormFieldContext';
import { handleEnterAsTabToNext } from 'src/forms/utils';
import { PickerValueT, ValuePicker } from 'src/utils/components/ValuePicker';
import { useScheduledCall } from 'src/utils/useScheduledCall';

type PropsT<ValueT> = {
  isMulti: boolean;
  isCreatable: boolean;
  pickableValues: ValueT[];
  submitOnChange?: boolean;
  labelFromValue: (value: any) => string;
  [k: string]: any;
};

export const ValuePickerField = observer(<ValueT,>(props: PropsT<ValueT>) => {
  const formState = useFormStateContext();
  const fieldContext = useFormFieldContext();
  const formValue = formState.values[fieldContext.fieldName];
  const scheduleSubmit = useScheduledCall(formState.submit);

  const saveChanges = (value: any, { action }: any) => {
    const toPickableValue = (value: PickerValueT) => {
      return value.__isNew__ ? value : value.value;
    };

    const pickableValue = props.isMulti
      ? (value || []).map(toPickableValue)
      : toPickableValue(value);

    formState.setValue(fieldContext.fieldName, pickableValue);
    if (props.submitOnChange) {
      scheduleSubmit();
    }
  };

  return (
    <ValuePicker
      {...props}
      name={fieldContext.fieldName}
      placeholder={fieldContext.label}
      pickableValue={formValue}
      onChange={saveChanges}
      onKeyDown={(e: any) => {
        if (props.tabOnEnter ?? true) {
          handleEnterAsTabToNext(e, false);
        }
        if (props.onKeyDown) {
          props.onKeyDown(e);
        }
      }}
    ></ValuePicker>
  );
});
