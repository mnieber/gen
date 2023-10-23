import { mergeLeft } from 'ramda';
import { useLocation, useParams } from 'react-router-dom';
import { useSearchParams } from '/src/utils/hooks/useSearchParams';
import { ObjT } from '/src/utils/types';

export const useSearchAndUrlParams = (): ObjT => {
  const params = useParams();
  const location = useLocation();
  const { all: searchParams } = useSearchParams(location);
  return mergeLeft(params, searchParams);
};
