import { observer } from 'mobx-react-lite';
import { withDefaultProps } from '/src/app/defaultProps';
import { cn } from '/src/utils/classnames';

// Import styles
import './LoaderBar.scss';

export type PropsT = {
  className?: any;
};

export const DefaultProps = {};

export const LoaderBar = observer(
  withDefaultProps((props: PropsT & typeof DefaultProps) => {
    return <div className={cn('LoaderBar', props.className)}></div>;
  }, DefaultProps)
);
