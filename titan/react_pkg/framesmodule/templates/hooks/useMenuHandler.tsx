import * as R from 'ramda';
import React from 'react';
import UIkit from '/src/frames/styles/uikit';

export const useMenuHandler = () => {
  const _ref = React.useRef(null);
  const [menuPos, setMenuPos] = React.useState<number>(0);

  const closeDropDown = () => {
    UIkit.dropdown(_ref.current as any).hide(false);
  };

  const openDropDown = () => {
    UIkit.dropdown(_ref.current as any).show();
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

  const handleContextMenu = (pos: number) => (e: any) => {
    setMenuPos(pos);
    openDropDown();
    e.preventDefault();
  };

  const menuTrigger = <div key="menuTrigger"></div>;
  const insertMenuDiv = (itemDivs: any[], menuDiv: any) => {
    return R.insertAll(
      R.clamp(0, itemDivs.length, menuPos),
      [menuTrigger, menuDiv],
      itemDivs
    );
  };

  return {
    closeDropDown,
    openDropDown,
    ref,
    handleContextMenu,
    insertMenuDiv,
    menuPos,
  };
};
