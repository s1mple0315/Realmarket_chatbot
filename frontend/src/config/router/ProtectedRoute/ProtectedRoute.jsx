import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { authState } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");

    if (!storedToken) {
      navigate("/login", { replace: true });
    }
  }, [navigate]);

  if (authState.isAuthenticated) {
    return children;
  }

  return null;
};

export default ProtectedRoute;
