import jQuery from 'jquery';
import React from 'react';
import UIkit from 'uikit';

export const useMenuRef = () => {
  const _ref = React.useRef(null);

  const closeDropDown = () => {
    jQuery(_ref.current as any).hide();
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
