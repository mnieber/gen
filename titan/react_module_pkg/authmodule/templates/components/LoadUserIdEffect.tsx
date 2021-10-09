import React from 'react';
import { loadUserId } from 'src/api/authApi';
import { EffectWithoutArgs } from 'src/utils/components';

export const LoadUserIdEffect: React.FC = () => {
  return (
    <EffectWithoutArgs
      f={() => {
        loadUserId();
      }}
    />
  );
};
