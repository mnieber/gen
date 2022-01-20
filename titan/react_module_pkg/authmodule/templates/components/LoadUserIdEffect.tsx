import React from 'react';
import { useLoadUserId } from 'src/api/authApi';
import { EffectWithoutArgs } from 'src/utils/components';

export const LoadUserIdEffect: React.FC = () => {
  const loadUserId = useLoadUserId();

  return (
    <EffectWithoutArgs
      f={() => {
        if (loadUserId.isIdle) {
          loadUserId.mutateAsync();
        }
      }}
    />
  );
};
