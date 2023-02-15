import { EndpointData } from 'src/api/EndpointData';
import { ObjT } from 'src/utils/types';

export class QueryData extends EndpointData {
  query: ObjT = {};

  public toString = (): string => {
    return `QueryData`;
  };
}
