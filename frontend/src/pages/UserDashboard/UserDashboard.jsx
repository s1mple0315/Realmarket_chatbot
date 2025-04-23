import { Outlet } from "react-router-dom";
import DashboardNavbar from "../../components/DashboardNavbar/DashboardNavbar";
import styles from "./UserDashboard.module.css";

const UserDashboard = () => {
  return (
    <div className={`${styles.userDashboardWrapper} d-flex`}>
      <div className={styles.userDashboardNavbar}>
        <DashboardNavbar />
      </div>

      <div className={styles.userDashboardContent}>
        <Outlet />
      </div>
    </div>
  );
};

export default UserDashboard;
