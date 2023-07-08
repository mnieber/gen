import { ObjT } from '/src/utils/types';

export function mergeClickHandlers(clickHandlers: ObjT[]) {
  return {
    onMouseDown: (e: any) => {
      for (const clickHandler of clickHandlers) {
        if (clickHandler.onMouseDown) {
          clickHandler.onMouseDown(e);
        }
      }
    },
    onMouseUp: (e: any) => {
      for (const clickHandler of clickHandlers) {
        if (clickHandler.onMouseUp) {
          clickHandler.onMouseUp(e);
        }
      }
    },
    onClick: (e: any) => {
      for (const clickHandler of clickHandlers) {
        if (clickHandler.onClick) {
          clickHandler.onClick(e);
        }
      }
    },
  };
}
