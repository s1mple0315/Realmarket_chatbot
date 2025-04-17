import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authState, setAuthState] = useState({
    isAuthenticated: false,
    access_token: null,
    token_type: null,
  });

  useEffect(() => {
    // Initialize authState from localStorage
    const storedToken = localStorage.getItem("access_token");
    const storedTokenType = localStorage.getItem("token_type");

    if (storedToken && storedTokenType) {
      setAuthState({
        isAuthenticated: true,
        access_token: storedToken,
        token_type: storedTokenType,
      });
    }
  }, []);

  useEffect(() => {
    console.log("Updated authState:", authState); // Logs whenever authState changes
  }, [authState]);

  const login = ({ access_token, token_type }) => {
    if (!access_token || !token_type) {
      throw new Error("Invalid token provided.");
    }

    setAuthState({
      isAuthenticated: true,
      access_token,
      token_type,
    });

    localStorage.setItem("access_token", access_token);
    localStorage.setItem("token_type", token_type);
  };

  const logout = () => {
    setAuthState({
      isAuthenticated: false,
      access_token: null,
      token_type: null,
    });

    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");
  };

  return (
    <AuthContext.Provider value={{ authState, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
