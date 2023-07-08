import { merge } from 'ramda';
import { useParams } from 'react-router-dom';
import { useSearchParams } from '/src/utils/hooks/useSearchParams';
import { ObjT } from '/src/utils/types';

export const useSearchAndUrlParams = (): ObjT => {
  const params = useParams();
  const { all: searchParams } = useSearchParams();
  return merge(params, searchParams);
};
