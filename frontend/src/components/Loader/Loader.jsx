import React from "react";
import styles from "./Loader.module.css"; // Import the CSS Module

const Loader = () => {
  return (
    <div className={styles.loaderWrapper}>
      <div>
        <svg height={0} width={0}>
          <defs>
            <filter
              colorInterpolationFilters="sRGB"
              height="200%"
              y="-50%"
              width="200%"
              x="-50%"
              id="goo"
            >
              <feGaussianBlur
                result="blur"
                stdDeviation={8}
                in="SourceGraphic"
              />
              <feColorMatrix
                result="cm"
                values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 21 -7"
                mode="matrix"
                in="blur"
              />
            </filter>
          </defs>
        </svg>
        <svg height={180} width={320} viewBox="0 0 320 180">
          <g filter="url(#goo)">
            <circle
              cy={90}
              cx={160}
              r={24}
              fill="#275EFE"
              className={`${styles.circle}`}
            />
            <circle
              cy={90}
              cx={160}
              r={24}
              fill="#275EFE"
              className={`${styles.circle} ${styles.right}`}
            />
          </g>
        </svg>
      </div>
    </div>
  );
};

export default Loader;
