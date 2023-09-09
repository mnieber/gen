import { ButtonPropsT } from '/src/frames/components/ButtonPropsT';
import {
  DefaultDialogButtonTrim,
  DialogButtonTrimT,
} from '/src/frames/components/DialogButton/trim';
import { Icon } from '/src/frames/components/Icon';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';
import { getMode, getModeCn } from '/src/utils/trim';

// Import styles
import './DialogButton.scss';

export type PropsT = {
  className?: any;
  trim?: DialogButtonTrimT;
  danger?: boolean;
  dataCy?: string;
  disabled?: boolean;
  iconName?: string;
  label: string;
} & ButtonPropsT;

export type DialogButtonPropsT = PropsT;

export const DialogButton = (props: PropsT) => {
  const {
    className,
    danger,
    trim: propsTrim,
    dataCy,
    disabled,
    iconName,
    label,
    ...rest
  } = props;

  const trim = propsTrim ?? DefaultDialogButtonTrim;
  const mode = getMode(trim, {
    danger,
    disabled,
  });

  return (
    /*
    🔳 DialogButton 🔳
    */
    <button
      className={cn(
        trim.base.componentName,
        'DialogButton',
        [
          getModeCn(mode.root),
          'select-none',
          {
            'DialogButton--disabled': disabled,
            'DialogButton--danger': danger,
          },
        ],
        [iconName ? L.row.skewer() : '', className]
      )}
      data-cy={dataCy}
      {...rest}
    >
      {iconName && <Icon className={getModeCn(mode.Icon)} name={iconName} />}
      {label}
    </button>
  );
};
