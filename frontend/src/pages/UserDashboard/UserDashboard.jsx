import DashboardNavbar from "../../components/DashboardNavbar/DashboardNavbar";
import styles from "./UserDashboard.module.css";

const UserDashboard = () => {
  return (
    <div className={styles.userDashboardWrapper}>
      <DashboardNavbar />
    </div>
  );
};

export default UserDashboard;
