import styles from "./DropdownButton.module.css";

const DropdownButton = () => {
  return (
    <button className={styles.dropdownButton}>
      <span>Записать на консультацию</span>
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={styles.chevronIcon}
      >
        <path
          d="M6 9L12 15L18 9"
          stroke="#6945ed"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </button>
  );
};

export default DropdownButton;
