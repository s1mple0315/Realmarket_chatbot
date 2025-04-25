import styles from "./ApplicationItem.module.css";

const ApplicationItem = ({ title, status, timestamp, unread }) => {
  return (
    <div
      className={`${styles.applicationItem} d-flex align-items-center justify-content-between`}
    >
      <div className="d-flex">
        <div className={styles.applicationItemStatus}>
          {unread && <span style={{ backgroundColor: "#6945ed" }}></span>}
        </div>
        <div
          className={`${styles.applicationItemText} d-flex flex-column gap-1`}
        >
          <h3>{title}</h3>
          <p>Статус заявки: {status}</p>
        </div>
      </div>
      <div className={styles.applicationItemTime}>
        <p>{timestamp}</p>
      </div>
    </div>
  );
};

export default ApplicationItem;
