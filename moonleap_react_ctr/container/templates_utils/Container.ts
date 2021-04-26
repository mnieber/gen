import { forEach } from "lodash/fp";

export class Container {
  _cleanUpFunctions: Function[] = [];

  addCleanUpFunction(f) {
    this._cleanUpFunctions.push(f);
  }

  destroy() {
    forEach((x) => x(), this._cleanUpFunctions);
  }
}
