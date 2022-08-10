import { makeObservable, observable } from 'mobx';
import { ObjT } from 'src/utils/types';

export class QueryData {
  query: ObjT = {};
  @observable data: ObjT | undefined = undefined;
  @observable status: string = '';

  constructor() {
    makeObservable(this);
  }
}
