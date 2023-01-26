import React from 'react';
import UIkit from 'src/frames/styles/uikit';

export const useMenuRef = () => {
  const _ref = React.useRef(null);

  const closeDropDown = () => {
    UIkit.dropdown(_ref.current as any).hide(false);
  };

  const ref = (elm: any) => {
    _ref.current = elm;
    UIkit.dropdown(elm, {
      animation: 'uk-animation-slide-top-small',
      duration: 100,
      mode: 'click',
      'delay-hide': 100,
    });
  };

  return {
    closeDropDown,
    ref,
  };
};
