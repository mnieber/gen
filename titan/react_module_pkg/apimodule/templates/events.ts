import { EventT } from 'src/utils/events';
import { RST } from 'src/utils/RST';

export type LoadDataEventT = EventT & {
  payload: EventT['payload'] & {
    state: RST
  }
};
