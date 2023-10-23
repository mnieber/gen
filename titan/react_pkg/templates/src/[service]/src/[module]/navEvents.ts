import { navHandler } from 'react-nav-handler';

export const navToFoo = (bar: string): void =>
  navHandler.getNavFn('navToFoo', navToFoo)(bar);
