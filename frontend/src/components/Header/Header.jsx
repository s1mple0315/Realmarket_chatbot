import { NavLink } from "react-router-dom";
import AppLogo from "../../icons/AppLogo";
import UserIcon from "../../icons/UserIcon";

import styles from "./Header.module.css";

const Header = () => {
  return (
    <header
      className={`${styles.header} d-flex justify-content-between align-items-center`}
    >
      <div className={styles.logo}>
        <AppLogo />
      </div>
      <nav className={styles.nav}>
        <ul className={`${styles.navList} d-flex`}>
          <li>
            <NavLink to="/">Продукты</NavLink>
          </li>
          <li>
            <NavLink to="/">Тарифы</NavLink>
          </li>
          <li>
            <NavLink to="/">Кейсы</NavLink>
          </li>
        </ul>
      </nav>
      <div className={`${styles.authButtons} d-flex`}>
        <button>
          <UserIcon /> Войти
        </button>
        <button>Попробовать бесплатно</button>
      </div>
    </header>
  );
};

export default Header;
