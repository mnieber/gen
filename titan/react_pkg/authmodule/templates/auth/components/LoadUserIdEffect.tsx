import React from 'react';
import { useStore } from 'src/app/components/useStore';
import { EffectWithoutArgs } from 'src/utils/components';

export const LoadUserIdEffect: React.FC = () => {
  const { authStore } = useStore();

  return (
    <EffectWithoutArgs
      f={() => {
        authStore.loadUserId();
      }}
    />
  );
};
