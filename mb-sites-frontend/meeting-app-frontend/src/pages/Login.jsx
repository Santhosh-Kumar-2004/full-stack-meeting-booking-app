import { useState } from "react";
import { toast } from "react-toastify";
import { useNavigate, Link } from "react-router-dom";
import "../styles/Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      toast.info("Please fill in all fields");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json(); // ✅ must be done before checking ok

      if (!response.ok) {
        toast.error(data.detail || "Invalid email or password");
        return;
      }

      // ✅ Clear any old user/session data
      localStorage.clear();

      // ✅ Save new token
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
      } else if (data.token) {
        localStorage.setItem("token", data.token);
      }

      // ✅ Optionally save user info (if backend returns)
      if (data.user) {
        localStorage.setItem("currentUser", JSON.stringify(data.user));
      }

      toast.success("Login successful!");
      navigate("/"); // redirect after login

    } catch (error) {
      console.error("Error during login:", error);
      toast.error("Something went wrong. Please check your connection.");
    }
  };

  return (
    <div className="register-page">
      <div className="register-card">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            required
          />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            required
          />
          <button type="submit" className="btn-primary">
            Login
          </button>
          <p className="register-link">
            Don’t have an account? <Link to="/register">Register</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;
