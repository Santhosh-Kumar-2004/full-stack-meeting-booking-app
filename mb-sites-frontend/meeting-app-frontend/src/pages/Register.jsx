import React, { useState } from "react";
import "../styles/Register.css";
import { Link } from "react-router-dom";

import { toast } from "react-toastify";

const Register = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const required_fields = async () => {
    if (formData.name && formData.email && formData.password) {
        // All required fields are filled
        console.log("All required fields are filled.");
        toast.info("All required fields are filled!");
    } else {
        // Some required fields are missing
        console.log("Some required fields are missing.");
        toast.error("Some required fields are missing.");
    }
};

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Registration failed");
      }

      const data = await response.json();
    //   setMessage("✅ Registration successful!");
      toast.success("Registered successfully!");
      setFormData({ name: "", email: "", password: "" });
    } catch (error) {
    //   setMessage(`❌ ${error.message}`);
      toast.error(`${error.message}`);
    }
  };

  return (
    <div className="register-page">
      <div className="register-card">
        <h2>Create Account</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <button type="submit" className="btn-primary" onClick={required_fields}>
            Register
          </button>
          <p>Already have an account? <Link to="/login">Login</Link></p>
        </form>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
};

export default Register;
