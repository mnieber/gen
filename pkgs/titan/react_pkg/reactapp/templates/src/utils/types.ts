export type ObjT = { [key: string]: any };

export const isString = (x: any) => {
  return typeof x === 'string' || x instanceof String;
};
