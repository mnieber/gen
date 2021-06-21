import React from 'react';
import { rsStore } from 'src/api/ResourceStatesStore';

import { isErroredRS, isResetRS, isUpdatingRS, LoadingT } from 'src/utils/RST';

type PropsT = {
  resourceUrl: string;
  renderUpdating?: (updating_state: LoadingT) => JSX.Element;
  renderErrored?: (message: string) => JSX.Element;
};

// TODO better default renders
const defaultRenderErrored = (message: string) => {
  return <div>Error{message !== undefined && `: ${message}`}</div>;
};
const defaultRenderUpdating = () => {
  return <div>Loading...</div>;
};

export const getResourceView = (props: PropsT) => {
  const renderErrored = props.renderErrored ?? defaultRenderErrored;
  const renderUpdating = props.renderUpdating ?? defaultRenderUpdating;
  const renderReset = () => {
    return <React.Fragment />;
  };

  const rs = rsStore.getState(props.resourceUrl);
  return isErroredRS(rs)
    ? renderErrored(rs.message)
    : isUpdatingRS(rs)
    ? renderUpdating(rs.updating_state)
    : isResetRS(rs)
    ? renderReset()
    : undefined;
};
