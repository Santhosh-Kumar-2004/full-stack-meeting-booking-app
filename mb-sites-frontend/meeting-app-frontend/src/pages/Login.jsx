import { useState } from "react";
// import axios from "axios";
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
            const response = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            //   const response = await axios.post("http://localhost:8000/auth/login", formData);
            const { access_token } = response.data;

            localStorage.setItem("token", access_token);
            toast.success("Login successful!");
            navigate("/dashboard"); // you can change this later to home/profile etc.

        } catch (error) {
            if (error.response && error.response.status === 401) {
                toast.error("Invalid email or password");
            } else {
                toast.error("Login failed. Please try again.");
            }
        }
    };

    return (
        <div className="register-page">
            <div className="register-card">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>

                    {/* <div className="form-group"> */}
                        {/* <label>Email</label> */}
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Enter your email"
                            required
                        />
                    {/* </div> */}

                    {/* <div className="form-group"> */}
                        {/* <label>Password</label> */}
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Enter your password"
                            required
                        />
                    {/* </div> */}

                    <button type="submit" className="btn-primary">Login</button>

                    <p className="register-link">
                        Don’t have an account? <Link to="/register">Register</Link>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default Login;
