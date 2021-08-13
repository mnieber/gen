import { ObjT } from 'src/utils/types';

export class EventTopic {
  text: string;

  constructor(text: string) {
    this.text = text;
  }
}

export type EventT = {
  payload: ObjT;
  topic: EventTopic;
};
