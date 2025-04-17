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
        <div>
          <h3>Sberbank Marketing</h3>
          <span>Тариф: Realboss</span>
        </div>
        <ul>
          <li>
            <NavLink ></NavLink>
            <StatsIcon /> Сводка
          </li>
          <li>
            <StatsIcon /> Диалоги
          </li>
          <li>
            <StatsIcon /> Интеграция
          </li>
          <li>
            <StatsIcon /> Заявки
          </li>
          <li>
            <StatsIcon /> Мой RealBot
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
