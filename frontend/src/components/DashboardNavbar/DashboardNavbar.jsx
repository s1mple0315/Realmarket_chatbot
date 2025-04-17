import { NavLink } from "react-router-dom";

import StatsIcon from "../../icons/StatsIcon";
import styles from "./DashboardNavbar.module.css";

const DashboardNavbar = () => {
  return (
    <div className={styles.dashboardNavbarWrapper}>
      <nav className={styles.dashboardNavbar}>
        <div
          className={`${styles.avatar} d-flex justify-content-between align-items-top`}
        ></div>
        <div className={`${styles.userInfo} d-flex flex-column`}>
          <h3>Sberbank Marketing</h3>
          <span>Тариф: Realboss</span>
        </div>
        <ul className={styles.navList}>
          <li>
            <NavLink
              to="/dashboard/stats"
              className={({ isActive }) => (isActive ? styles.active : "")}
            >
              <StatsIcon /> Сводка
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/dashboard/dialogs"
              className={({ isActive }) => (isActive ? styles.active : "")}
            >
              <StatsIcon /> Диалоги
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/dashboard/integration"
              className={({ isActive }) => (isActive ? styles.active : "")}
            >
              <StatsIcon /> Интеграция
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/dashboard/applications"
              className={({ isActive }) => (isActive ? styles.active : "")}
            >
              <StatsIcon /> Заявки
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/dashboard/my-realbot"
              className={({ isActive }) => (isActive ? styles.active : "")}
            >
              <StatsIcon /> Мой RealBot
            </NavLink>
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
