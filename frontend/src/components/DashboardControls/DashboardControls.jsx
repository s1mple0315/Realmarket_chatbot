import { useState } from "react";
import styles from "./DashboardControls.module.css";
import Calendar from "../../icons/Calendar";

const DashboardControls = ({ onTabChange }) => {
  const [activeTab, setActiveTab] = useState("today");
  const tabs = [
    { id: "today", label: "Сегодня" },
    { id: "week", label: "Неделя" },
    { id: "month", label: "Месяц" },
  ];

  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
    onTabChange(tabId);
  };

  const currentTime = new Date().toLocaleString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
    day: "2-digit",
    month: "2-digit",
    year: "2-digit",
  });

  return (
    <div className={styles.controlsWrapper}>
      <div className={styles.tabsContainer}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`${styles.tab} ${
              activeTab === tab.id ? styles.active : ""
            }`}
            onClick={() => handleTabClick(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className={styles.timeContainer}>
        <Calendar /> <span>{currentTime}</span>
      </div>
    </div>
  );
};

export default DashboardControls;
