import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { lazy, Suspense } from "react";

import Loader from "../../components/Loader/Loader";
import AuthPage from "../../pages/AuthPage/AuthPage";
import HomePage from "../../pages/HomePage/HomePage";

// const HomePage = lazy(() => import("../../pages/HomePage/HomePage"));
const UserDashboard = lazy(() =>
  import("../../pages/UserDashboard/UserDashboard")
);

const AppRouter = () => {
  return (
    <AuthProvider>
      <Router>
        <Suspense fallback={<Loader />}>
          <Routes>
            <Route path="/" exact element={<HomePage />} />
            <Route path="/login" element={<AuthPage />} />
            <Route path="/dashboard" element={<UserDashboard />} />
          </Routes>
        </Suspense>
      </Router>
    </AuthProvider>
  );
};

export default AppRouter;
