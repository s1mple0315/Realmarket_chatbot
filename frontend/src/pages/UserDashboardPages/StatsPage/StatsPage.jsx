import styles from "./StatsPage.module.css";
import { useState } from "react";
import DashboardControls from "../../../components/DashboardControls/DashboardControls";
import DashboardStats from "../../../components/DashboardStats/DashboardStats";

const StatsPage = () => {
  const [activeTab, setActiveTab] = useState("today");

  return (
    <div className={styles.dashboard}>
      <div className={styles.mainContent}>
        <div className="d-flex align-items-center justify-content-between">
          <h2 className={styles.title}>Сводка</h2>
          <div className="d-flex align-items-center gap-3">
            <DashboardControls onTabChange={setActiveTab} />
            <span className={styles.dateTime}>01:03 - 12.04.25</span>
          </div>
        </div>
        <DashboardStats activeTab={activeTab} />
      </div>
    </div>
  );
};

export default StatsPage;
