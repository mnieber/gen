import { EventT } from 'src/utils/events';
import { RST } from 'src/utils/RST';

export type LoadDataEventT = EventT & {
  state: RST;
};
