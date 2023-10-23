import { action, makeObservable, observable } from 'mobx';
import { useBuilder } from '/src/utils/hooks';
import { ObjT } from '/src/utils/types';

export type MutationStatusT = 'idle' | 'loading' | 'success' | 'error';

export type ArgsT = {
  mutationFn: (args: any) => Promise<any> | void;
  onMutate?: (args: any) => Promise<any> | void;
  onSuccess?: (response: ObjT, args: any) => Promise<any> | void;
  onError?: (args: any) => void;
};

export class ObservableMutation {
  status = 'idle';
  mutationFn: (args: any) => Promise<any> | void;
  onMutate?: (args: any) => Promise<any> | void;
  onSuccess?: (response: ObjT, args: any) => Promise<any> | void;
  onError?: (args: any) => void;

  setStatus = (status: MutationStatusT) => {
    this.status = status;
  };

  mutateAsync = (args: any) => {
    this.setStatus('loading');
    return Promise.resolve(this.onMutate ? this.onMutate(args) : undefined)
      .then(() => this.mutationFn(args))
      .then((response: any) => {
        return Promise.resolve(
          this.onSuccess ? this.onSuccess(response, args) : undefined
        ).then(() => {
          this.setStatus('success');
          return response;
        });
      })
      .catch((error: any) => {
        return Promise.resolve(
          this.onError ? this.onError(error) : undefined
        ).then(() => {
          this.setStatus('error');
          return error;
        });
      });
  };

  constructor(args: ArgsT) {
    this.mutationFn = args.mutationFn;
    this.onSuccess = args.onSuccess;
    this.onError = args.onError;
    this.onMutate = args.onMutate;

    makeObservable(this, {
      status: observable,
      setStatus: action,
    });
  }
}

export const isRunning = (observableMutation: ObservableMutation) => {
  return observableMutation.status === 'loading';
};

export const useObservableMutation = (args: ArgsT) => {
  return useBuilder(() => new ObservableMutation(args));
};
