import { useFormStateContext } from 'react-form-state-context';
import {
  DefaultDialogButtonTrim,
  DialogButton,
  DialogButtonPropsT,
  DialogButtonS,
} from '/src/frames/components/DialogButton';
import { createTrim } from '/src/utils/trim';

export type PropsT = DialogButtonPropsT;

export const FormSaveButton = (props: PropsT) => {
  const formState = useFormStateContext();
  const disabled = props.disabled || formState.getFlag('submitting');

  return (
    <DialogButton
      trim={MainViewDialogButtonTrim}
      onClick={(e: any) => {
        e.preventDefault();
        formState.submit();
      }}
      disabled={disabled}
      {...props}
    />
  );
};

const MainViewDialogButtonTrim = createTrim(DefaultDialogButtonTrim, {
  base: {
    componentName: 'FormSaveButton-DialogButton',
    root: {
      color: DialogButtonS.color.blueWithDarkText(),
    },
  },
  danger: {
    root: {
      color: DialogButtonS.color.redWithWhiteText(),
    },
  },
  disabled: {
    root: {
      color: DialogButtonS.color.grayBackground(),
    },
  },
});
