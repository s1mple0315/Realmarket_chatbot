import StatsIcon from "../../icons/StatsIcon";
import styles from "./DashboardNavbar.module.css";

const DashboardNavbar = () => {
  return (
    <div className={styles.dashboardNavbarWrapper}>
      <nav className={styles.dashboardNavbar}>
        <div
          className={`${styles.avatar} d-flex justify-content-between align-items-top`}
        ></div>
        <div>
          <h3>Sberbank Marketing</h3>
          <button>Тариф: Realboss</button>
        </div>
        <ul>
          <li>
            <StatsIcon /> Сводка
          </li>
          <li>
            <StatsIcon /> Сводка
          </li>
          <li>
            <StatsIcon /> Сводка
          </li>
          <li>
            <StatsIcon /> Сводка
          </li>
          <li>
            <StatsIcon /> Сводка
          </li>
        </ul>
        <div>
          <button>Поддержка</button>
          <button>Выйти</button>
        </div>
      </nav>
    </div>
  );
};

export default DashboardNavbar;
