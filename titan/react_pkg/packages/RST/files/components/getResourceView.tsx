import React from 'react';
import { rsMap } from 'src/api/ResourceStateMap';
import { flags } from 'src/app/flags';
import { log } from 'src/utils/logging';
import { isErroredRS, isResetRS, isUpdatingRS, LoadingT } from 'src/utils/RST';

type PropsT = {
  resUrl: string | undefined;
  res: any;
  renderUpdating?: (updatingState: LoadingT) => JSX.Element;
  renderErrored?: (message: string) => JSX.Element;
};

const defaultRenderErrored = (message: string) => {
  return <div>Error{message !== undefined && `: ${message}`}</div>;
};
const defaultRenderUpdating = () => {
  return <div>Loading...</div>;
};

const renderReset = () => {
  return <React.Fragment />;
};

export const getResourceView = (props: PropsT) => {
  if (!props.resUrl && !props.res) return renderReset();
  if (!props.resUrl) return undefined;

  const renderErrored = props.renderErrored ?? defaultRenderErrored;
  const renderUpdating = props.renderUpdating ?? defaultRenderUpdating;

  if (!rsMap.has(props.resUrl)) {
    if (flags.logResourceView) {
      log('getResourceView: unknown url', props.resUrl);
    }
  }

  const rs = rsMap.get(props.resUrl);
  return isErroredRS(rs)
    ? renderErrored(rs.message)
    : isUpdatingRS(rs)
    ? renderUpdating(rs.updatingState)
    : isResetRS(rs)
    ? renderReset()
    : undefined;
};
