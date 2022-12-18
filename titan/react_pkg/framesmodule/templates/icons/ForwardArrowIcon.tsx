import 'src/frames/components/Icon.scss';

export const ForwardArrowIcon = () => {
  return (
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g fill="none" fillRule="evenodd">
        <path d="M0 0h24v24H0z" />
        <path
          className="Icon"
          fillRule="nonzero"
          d="m12 20-1.425-1.4 5.6-5.6H4v-2h12.175l-5.6-5.6L12 4l8 8z"
        />
      </g>
    </svg>
  );
};
