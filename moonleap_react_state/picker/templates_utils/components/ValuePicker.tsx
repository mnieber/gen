import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';
import { isNil } from 'lodash/fp';
import { observer } from 'mobx-react';

import { handleEnterAsTabToNext } from 'src/utils/form_utils';

export interface PickerValueT {
  value: any;
  label: string;
  __isNew__?: boolean;
}

type PropsT<ValueT> = {
  isMulti: boolean;
  isCreatable: boolean;
  pickableValues: ValueT[];
  pickableValue: ValueT;
  labelFromValue: (value: any) => string;
  [k: string]: any;
};

export const ValuePicker = observer(
  <ValueT, ConcretePropsT extends PropsT<ValueT>>(
    props: ConcretePropsT
  ): JSX.Element => {
    const {
      isMulti,
      isCreatable,
      pickableValue,
      pickableValues,
      labelFromValue,
      ...others
    } = props;

    const toPickerValue = (pickableVal: any) => {
      return pickableVal.__isNew__
        ? pickableVal
        : {
            value: pickableVal,
            label: labelFromValue(pickableVal),
          };
    };

    const options = pickableValues.map(toPickerValue);

    const pickerProps = {
      isMulti: isMulti,
      options,
      value: isNil(pickableValue)
        ? undefined
        : isMulti
        ? (pickableValue as any).map(toPickerValue)
        : toPickerValue(pickableValue),
      onKeyDown: (e: any) => {
        if (props.tabOnEnter ?? true) {
          handleEnterAsTabToNext(e, false);
        }
        if (others.onKeyDown) {
          others.onKeyDown(e);
        }
      },
      ...others,
    };

    const picker = isCreatable ? (
      <CreatableSelect {...pickerProps} />
    ) : (
      <Select {...pickerProps} />
    );

    return <div style={{ zIndex: others.zIndex }}>{picker}</div>;
  }
);
