import { useState } from "react";
import DashboardControls from "../../../components/DashboardControls/DashboardControls";
import ApplicationItem from "../../../components/ApplicationItem/ApplicationItem";
import styles from "./ApplicationPage.module.css";

const mockApplications = [
  {
    title: "Разработка сайта",
    status: "входящая",
    timestamp: "13.04.25",
    unread: true,
  },
  {
    title: "Создание логотипа",
    status: "в обработке",
    timestamp: "12.04.25",
    unread: true,
  },
  {
    title: "SEO продвижение",
    status: "завершена",
    timestamp: "11.04.25",
    unread: false,
  },
  {
    title: "Мобильное приложение",
    status: "входящая",
    timestamp: "10.04.25",
    unread: false,
  },
  {
    title: "Дизайн интерфейса",
    status: "в обработке",
    timestamp: "09.04.25",
    unread: false,
  },
];

const ApplicationPage = () => {
  const [activeTab, setActiveTab] = useState("today");

  const totalApplications = mockApplications.length;
  const newApplications = mockApplications.filter((app) => app.unread).length;

  return (
    <div className={styles.applicationPage}>
      <div
        className={`${styles.applicationPageTitle} d-flex align-items-center justify-content-between`}
      >
        <h3>Заявки</h3>
        <DashboardControls onTabChange={setActiveTab} />
      </div>

      <div className={styles.applicationPageContent}>
        <h3>
          Заявок: {totalApplications} / Новых: {newApplications}
        </h3>
        <div className={styles.applicationList}>
          {mockApplications.map((app, index) => (
            <ApplicationItem
              key={index}
              title={app.title}
              status={app.status}
              timestamp={app.timestamp}
              unread={app.unread}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ApplicationPage;
