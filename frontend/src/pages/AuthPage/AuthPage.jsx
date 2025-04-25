import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { AuthContext } from "../../config/context/AuthContext";
import Footer from "../../components/Footer/Footer";
import Header from "../../components/Header/Header";

import styles from "./AuthPage.module.css";

const AuthPage = () => {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);

  const navigate = useNavigate();

  const toggleMode = () => {
    setIsLoginMode((prevMode) => !prevMode);
    setError(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const url = isLoginMode
        ? "http://localhost:8000/api/v1/auth/login"
        : "http://localhost:8000/api/v1/auth/register";

      const requestBody = new URLSearchParams({
        grant_type: "password",
        username: formData.username,
        password: formData.password,
      });

      const response = await axios.post(url, requestBody, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token, token_type } = response.data;

      if (access_token) {
        console.log(isLoginMode ? "Logged in!" : "Registered!");

        login({ access_token, token_type });
        navigate("/dashboard");
      } else {
        setError("An error occurred while processing the response.");
      }
    } catch (err) {
      setError("Something went wrong.");
    }
  };

  return (
    <div className={`${styles.pageContainer} d-flex flex-column`}>
      <Header />
      <div
        className={`${styles.authContainer} d-flex flex-column justify-content-center align-items-center`}
      >
        <h2>{isLoginMode ? "Вход в кабинет" : "Регистрация"}</h2>
        <form onSubmit={handleSubmit} className={styles.authForm}>
          <div>
            <input
              type="text"
              name="username"
              placeholder="+7 (___) ___-__-__"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <button type="submit">
            {isLoginMode ? "Войти в личный кабинет" : "Register"}
          </button>
        </form>
      </div>
      <Footer />
    </div>
  );
};

export default AuthPage;
