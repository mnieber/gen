import { cn } from '/src/utils/classnames';
import { ObjT } from '/src/utils/types';

// Import styles
import './Icon.scss';

export const icons: ObjT = {};

export type PropsT = {
  name: string;
  onClick?: () => void;
  className?: any;
};

export const Icon = (props: PropsT) => {
  const svg = icons[props.name] ?? <div>`${props.name} not found`</div>;
  return (
    <div className={cn('Icon', props.className)} onClick={props.onClick}>
      {svg}
    </div>
  );
};

export const IconS = {
  color: {
    gray: () => 'fill-gray-text',
    teal: () => 'fill-teal-primary',
    grayDarkest: () => 'fill-gray-darkest',
    blueDarkest: () => 'fill-blue-darkest',
    bluePrimary: () => 'fill-blue-primary',
    tealDark: () => 'fill-teal-dark',
    white: () => 'fill-white',
  },
  size: {
    s15: () => 'w-[15px] h-[15px]',
    s20: () => 'w-[20px] h-[20px] min-w-[20px]',
    s24: () => 'w-[24px] h-[24px]',
    s30: () => 'w-[30px] h-[30px] min-w-[30px]',
    s32: () => 'w-[32px] h-[32px] min-w-[32px]',
  },
};
