import UIkit from '/src/frames/styles/uikit';
import { cn } from '/src/utils/classnames';

// Import styles
import './Icon.scss';

export type PropsT = {
  name: string;
  ratio?: number;
  className?: any;
};

export const Icon = (props: PropsT) => {
  return (
    UIkit && (
      <div
        className={cn('Icon', '!mr-2', props.className)}
        data-uk-icon={`icon: ${props.name}; ratio: ${props.ratio ?? 1}`}
      />
    )
  );
};
