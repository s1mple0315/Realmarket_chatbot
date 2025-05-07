const ChatBotIndicator = () => {
  return (
    <svg
      width="34"
      height="34"
      viewBox="0 0 34 34"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g filter="url(#filter0_d_102_3793)">
        <rect
          x="2"
          width="30"
          height="30"
          rx="6"
          fill="white"
          shapeRendering="crispEdges"
        />
        <g clip-path="url(#clip0_102_3793)">
          <rect
            x="9.5"
            y="8.65384"
            width="13.8235"
            height="13.8462"
            rx="3"
            fill="#6945ED"
          />
          <path
            d="M23.1338 7.74561C23.7535 7.7457 24.2832 8.23879 24.2832 8.88428V10.9292C24.2832 11.5633 23.7574 12.0678 23.1338 12.0679H21.0527C20.4329 12.0679 19.9023 11.5747 19.9023 10.9292V8.88428C19.9023 8.25402 20.4174 7.74561 21.0527 7.74561H23.1338Z"
            fill="#6945ED"
            stroke="white"
          />
        </g>
      </g>
      <defs>
        <filter
          id="filter0_d_102_3793"
          x="0.0377359"
          y="0"
          width="33.9245"
          height="33.9245"
          filterUnits="userSpaceOnUse"
          colorInterpolationFilters="sRGB"
        >
          <feFlood flood-opacity="0" result="BackgroundImageFix" />
          <feColorMatrix
            in="SourceAlpha"
            type="matrix"
            values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
            result="hardAlpha"
          />
          <feOffset dy="1.96226" />
          <feGaussianBlur stdDeviation="0.981132" />
          <feComposite in2="hardAlpha" operator="out" />
          <feColorMatrix
            type="matrix"
            values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.05 0"
          />
          <feBlend
            mode="normal"
            in2="BackgroundImageFix"
            result="effect1_dropShadow_102_3793"
          />
          <feBlend
            mode="normal"
            in="SourceGraphic"
            in2="effect1_dropShadow_102_3793"
            result="shape"
          />
        </filter>
        <clipPath id="clip0_102_3793">
          <rect
            width="15"
            height="15"
            fill="white"
            transform="translate(9.5 7.5)"
          />
        </clipPath>
      </defs>
    </svg>
  );
};

export default ChatBotIndicator;
