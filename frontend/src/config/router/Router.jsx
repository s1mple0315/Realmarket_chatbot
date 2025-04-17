import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { lazy, Suspense } from "react";

import Loader from "../../components/Loader/Loader";
import AuthPage from "../../pages/AuthPage/AuthPage";
import HomePage from "../../pages/HomePage/HomePage";
import ProtectedRoute from "./ProtectedRoute/ProtectedRoute";

const UserDashboard = lazy(() =>
  import("../../pages/UserDashboard/UserDashboard")
);
const ApplicationPage = lazy(() =>
  import("../../pages/UserDashboardPages/ApplicationsPage/ApplicationPage")
);
const DialogsPage = lazy(() =>
  import("../../pages/UserDashboardPages/DialogsPage/DialogsPage")
);
const IntegrationPage = lazy(() =>
  import("../../pages/UserDashboardPages/IntegrationPage/IntegrationPage")
);
const MyRealbotPage = lazy(() =>
  import("../../pages/UserDashboardPages/MyRealbotPage/MyRealbotPage")
);
const StatsPage = lazy(() =>
  import("../../pages/UserDashboardPages/StatsPage/StatsPage")
);


const AppRouter = () => {
  return (
    <AuthProvider>
      <Router>
        <Suspense fallback={<Loader />}>
          <Routes>
            <Route path="/" exact element={<HomePage />} />
            <Route path="/login" element={<AuthPage />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <UserDashboard />
                </ProtectedRoute>
              }
            >
              <Route path="/dashboard/my-realbot" element={<MyRealbotPage />} />
              <Route
                path="/dashboard/applications"
                element={<ApplicationPage />}
              />
              <Route
                path="/dashboard/integration"
                element={<IntegrationPage />}
              />
              <Route path="/dashboard/dialogs" element={<DialogsPage />} />
              <Route path="/dashboard/stats" element={<StatsPage />} />
            </Route>
          </Routes>
        </Suspense>
      </Router>
    </AuthProvider>
  );
};

export default AppRouter;
