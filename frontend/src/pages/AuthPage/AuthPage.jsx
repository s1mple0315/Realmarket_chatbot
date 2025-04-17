import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { AuthContext } from "../../config/context/AuthContext";

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
    <div>
      <h2>{isLoginMode ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">{isLoginMode ? "Login" : "Register"}</button>
      </form>
      <button onClick={toggleMode}>
        Switch to {isLoginMode ? "Register" : "Login"}
      </button>
    </div>
  );
};

export default AuthPage;
