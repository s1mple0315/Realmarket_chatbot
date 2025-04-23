import styles from "./StatsContainer.module.css";

const StatsContainer = ({ title, children }) => {
  return (
    <div className={styles.container}>
      <h3 className={styles.title}>{title}</h3>
      <div className={styles.content}>{children}</div>
    </div>
  );
};

export default StatsContainer;
