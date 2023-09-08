export const breakpoints = {
  xs: '320px',
  small: '480px',
  medium: '768px',
  large: '976px',
  xlarge: '1280px',
};

export const L = {
  row: {
    skewer: () => 'flex flex-row items-center',
    banner: () => 'flex flex-row items-stretch',
    flagPole: () => 'flex flex-row items-start',
    revFlagPole: () => 'flex flex-row items-end',
  },
  col: {
    skewer: () => 'flex flex-col items-center',
    banner: () => 'flex flex-col items-stretch',
    flagPole: () => 'flex flex-col items-start',
    flagPoleRev: () => 'flex flex-col items-end',
  },
};
