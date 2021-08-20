import React from 'react';
import { rsMap } from 'src/api/ResourceStateMap';
import { isErroredRS, isResetRS, isUpdatingRS, LoadingT } from 'src/utils/RST';

type PropsT = {
  resUrl: string | undefined;
  renderUpdating?: (updatingState: LoadingT) => JSX.Element;
  renderErrored?: (message: string) => JSX.Element;
};

const defaultRenderErrored = (message: string) => {
  return <div>Error{message !== undefined && `: ${message}`}</div>;
};
const defaultRenderUpdating = () => {
  return <div>Loading...</div>;
};

export const getResourceView = (props: PropsT) => {
  if (!props.resUrl) return undefined;

  const renderErrored = props.renderErrored ?? defaultRenderErrored;
  const renderUpdating = props.renderUpdating ?? defaultRenderUpdating;
  const renderReset = () => {
    return <React.Fragment />;
  };

  const rs = rsMap.getRS(props.resUrl);
  return isErroredRS(rs)
    ? renderErrored(rs.message)
    : isUpdatingRS(rs)
    ? renderUpdating(rs.updatingState)
    : isResetRS(rs)
    ? renderReset()
    : undefined;
};
