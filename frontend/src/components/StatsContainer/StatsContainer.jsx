import styles from "./StatsContainer.module.css";

const StatsContainer = ({ title, children, className }) => {
  return (
    <div className={`${styles.container} ${className || ""}`}>
      <h3 className={styles.title}>{title}</h3>
      <div className={styles.content}>{children}</div>
    </div>
  );
};

export default StatsContainer;
