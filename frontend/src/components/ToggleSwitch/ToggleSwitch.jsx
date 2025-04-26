import styles from "./ToggleSwitch.module.css";

const ToggleSwitch = ({ checked, onChange }) => {
  return (
    <div className={styles.toggleContainer}>
      <input
        type="checkbox"
        id="toggle"
        className={styles.toggleInput}
        checked={checked}
        onChange={onChange}
      />
      <label htmlFor="toggle" className={styles.toggleLabel}></label>
    </div>
  );
};

export default ToggleSwitch;
