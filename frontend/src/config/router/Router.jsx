import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { lazy, Suspense } from "react";

import Loader from "../../components/Loader/Loader";

const HomePage = lazy(() => import("../../pages/HomePage/HomePage"));
const UserDashboard = lazy(() =>
  import("../../pages/UserDashboard/UserDashboard")
);

const Router = () => {
  return (
    <AuthProvider>
      <Router>
        <Suspense fallback={<Loader />}>
          <Routes>
            <Route path="/" exact component={<HomePage />} />
            <Route path="/login" component={<HomePage />} />
            <Route path="/dashboard" component={<UserDashboard />} />
          </Routes>
        </Suspense>
      </Router>
    </AuthProvider>
  );
};

export default Router;
