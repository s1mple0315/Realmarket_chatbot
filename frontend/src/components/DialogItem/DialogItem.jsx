import DialogsArrow from "../../icons/DialogsArrow";
import Checkmarks from "../../icons/Checkmarks";
import styles from "./DialogItem.module.css";

const DialogItem = ({
  userId,
  message,
  timestamp,
  readStatus,
  readTime,
  unread,
  onArrowClick,
}) => {
  return (
    <div
      className={`${styles.dialogItem} d-flex align-items-center justify-content-between`}
    >
      <div className="d-flex align-items-center">
        <div className={styles.dialogItemStatus}>
          {unread && <span style={{ backgroundColor: "#6945ed" }}></span>}
        </div>
        <div className={`${styles.dialogItemText} d-flex flex-column`}>
          <h3>{userId}</h3>
          <p>{message}</p>
        </div>
      </div>
      <div className="d-flex gap-2">
        <div className={`${styles.dialogItemTime} d-flex align-items-start`}>
          {readStatus && (
            <>
              <Checkmarks />
              <p>{readTime}</p>
            </>
          )}
          {!readStatus && <p>{timestamp}</p>}
        </div>
        <div className={styles.dialogItemButton}>
          <button
            onClick={onArrowClick}
            style={{ border: "none", background: "none" }}
          >
            <DialogsArrow />
          </button>
        </div>
      </div>
    </div>
  );
};

export default DialogItem;
