import React, { useState } from "react";
import axios from "axios";

const AuthPage = () => {
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);

  const toggleMode = () => {
    setIsLoginMode((prevMode) => !prevMode);
    setError(null);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const url = isLoginMode
        ? "http://localhost:8000/api/v1/auth/login"
        : "http://localhost:8000/api/v1/auth/register";

      const response = await axios.post(url, formData);

      if (response.data.success) {
        console.log(isLoginMode ? "Logged in!" : "Registered!");
      } else {
        setError(response.data.message || "An error occurred.");
      }
    } catch (err) {
      setError(err.response?.data?.message || "Something went wrong.");
    }
  };

  return (
    <div>
      <h2>{isLoginMode ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
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
