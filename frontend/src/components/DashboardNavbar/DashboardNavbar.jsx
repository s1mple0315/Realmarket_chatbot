import { NavLink } from "react-router-dom";

import StatsIcon from "../../icons/StatsIcon";
import LogoutIcon from "../../icons/LogoutIcon";
import BellIcon from "../../icons/BellIcon";
import SettingsIcon from "../../icons/SettingsIcon";

import styles from "./DashboardNavbar.module.css";

const DashboardNavbar = () => {
  return (
    <div className={styles.dashboardNavbarWrapper}>
      <nav className={styles.dashboardNavbar}>
        <div
          className={`${styles.avatar} d-flex justify-content-between align-items-top`}
        >
          <div className={styles.avatarLogo}>
            <img src="/assets/images/Dashboard/Logo/sber.png" alt="User Logo" />
          </div>
          <div className={styles.avatarSettings}>
            <div className={styles.avatarSettingsNews}>
              <BellIcon />
            </div>
            <div>
              <SettingsIcon />
            </div>
          </div>
        </div>
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
        <div className={`${styles.support} d-flex align-items-center gap-2`}>
          <button className={styles.supportButton}>Поддержка</button>
          <button className={styles.logoutButton}>
            <LogoutIcon />
          </button>
        </div>
      </nav>
    </div>
  );
};

export default DashboardNavbar;
