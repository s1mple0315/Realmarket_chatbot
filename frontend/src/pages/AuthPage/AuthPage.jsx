import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { AuthContext } from "../../config/context/AuthContext";
import Footer from "../../components/Footer/Footer";
import Header from "../../components/Header/Header";

import styles from "./AuthPage.module.css";

const AuthPage = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);

  const navigate = useNavigate();

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
      const url = "http://localhost:8000/api/v1/auth/login";

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
        console.log("Logged in!");
        login({ access_token, token_type });
        navigate("/dashboard");
      } else {
        setError("No access token received from the server.");
        console.log("Response data:", response.data);
      }
    } catch (err) {
      console.error("Login error:", err.response || err.message);
      setError(
        err.response?.data?.detail || "Failed to login. Please try again."
      );
    }
  };

  return (
    <div className={`${styles.pageContainer} d-flex flex-column`}>
      <Header />
      <div
        className={`${styles.authContainer} d-flex flex-column justify-content-center align-items-center`}
      >
        <h2>Вход в кабинет</h2>
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
          <button type="submit">Войти в личный кабинет</button>
          <img
            src="assets/images/Background/cube.png"
            className={styles.backgroundCube}
            alt="background-cube image"
          />
        </form>
      </div>
      <Footer />
    </div>
  );
};

export default AuthPage;
