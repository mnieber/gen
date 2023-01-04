import 'src/frames/components/Icon.scss';
import UIkit from 'uikit';

export const NewIcon = () => {
  return (
    UIkit && (
      <div className="NewIcon Icon" data-uk-icon="icon: check; ratio: 2"></div>
    )
  );
};
