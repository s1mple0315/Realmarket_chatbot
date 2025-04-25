import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardControls from "../../../components/DashboardControls/DashboardControls";
import DialogItem from "../../../components/DialogItem/DialogItem";
import styles from "./DialogsPage.module.css";

const mockDialogs = [
  {
    userId: "User-73",
    message: "Как мне зайти в личный кабинет если я забыл пароль?",
    timestamp: "14.04.25, 17:42",
    readStatus: true,
    readTime: "18:02",
    unread: true,
  },
  {
    userId: "User-71",
    message: "Спасио за ваш запрос я передал ваши контакты нашему менеджеру",
    timestamp: "14.04.25, 17:42",
    readStatus: true,
    readTime: "18:02",
    unread: true,
  },
  {
    userId: "User-36",
    message: "Кастыльный доступ только для пользователя с 80 lvl",
    timestamp: "14.04.25, 17:42",
    readStatus: false,
    readTime: null,
    unread: false,
  },
  {
    userId: "User-343",
    message: "Спасио за ваш запрос я передал ваши контакты нашему менеджеру",
    timestamp: "14.04.25, 17:42",
    readStatus: false,
    readTime: null,
    unread: false,
  },
  {
    userId: "User-46",
    message: "Как мне зайти в личный кабинет если я забыл пароль?",
    timestamp: "14.04.25, 17:42",
    readStatus: false,
    readTime: null,
    unread: false,
  },
  {
    userId: "User-26",
    message: "Кастыльный доступ только для пользователя с 80 lvl",
    timestamp: "14.04.25, 17:42",
    readStatus: false,
    readTime: null,
    unread: false,
  },
  {
    userId: "User-84",
    message: "Как мне зайти в личный кабинет если я забыл пароль?",
    timestamp: "14.04.25, 17:42",
    readStatus: false,
    readTime: null,
    unread: false,
  },
  {
    userId: "User-84",
    message: "Как мне зайти в личный кабинет если я забыл пароль?",
    timestamp: "14.04.25, 17:42",
    readStatus: false,
    readTime: null,
    unread: false,
  },
  {
    userId: "User-11",
    message: "Кастыльный доступ только для пользователя с 80 lvl",
    timestamp: "14.04.25, 17:42",
    readStatus: false,
    readTime: null,
    unread: false,
  },
];

const DialogsPage = () => {
  const [activeTab, setActiveTab] = useState("today");
  const navigate = useNavigate();

  const handleDialogClick = (userId) => {
    navigate(`/dialog/${userId}`);
  };

  return (
    <div className={styles.dialogsPage}>
      <div
        className={`${styles.dialogsPageTitle} d-flex align-items-center justify-content-between`}
      >
        <h2 className={styles.title}>Диалоги</h2>
        <DashboardControls onTabChange={setActiveTab} />
      </div>

      <div className={styles.dialogsPageContent}>
        <h3>Диаологов: 24 / Новых: 2</h3>
        {mockDialogs.map((dialog, index) => (
          <DialogItem
            key={index}
            userId={dialog.userId}
            message={dialog.message}
            timestamp={dialog.timestamp}
            readStatus={dialog.readStatus}
            readTime={dialog.readTime}
            unread={dialog.unread}
            onArrowClick={() => handleDialogClick(dialog.userId)}
          />
        ))}
      </div>
    </div>
  );
};

export default DialogsPage;
