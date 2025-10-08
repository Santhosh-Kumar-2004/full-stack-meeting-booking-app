import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "../styles/AllUsers.css";

const AllUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      toast.error("Please log in first");
      navigate("/login");
      return;
    }

    const fetchUsers = async () => {
      try {
        const response = await fetch("http://localhost:8000/auth/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.status === 403) {
          toast.error("Access denied: Admins only");
          navigate("/");
          return;
        }

        if (!response.ok) {
          throw new Error("Failed to fetch users");
        }

        const data = await response.json();
        setUsers(data);
      } catch (error) {
        console.error("Error fetching users:", error);
        toast.error("Something went wrong while fetching users");
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [navigate]);

  if (loading) {
    return (
      <div className="users-loading">
        <div className="loader"></div>
        <p>Loading users...</p>
      </div>
    );
  }

  return (
    <div className="users-page">
      <h1 className="users-title">All Registered Users</h1>
      <div className="users-grid">
        {users.length > 0 ? (
          users.map((user) => (
            <div key={user.id} className="user-card">
              <h2>{user.name}</h2>
              <p>{user.email}</p>
              <span className={`role ${user.role}`}>{user.role}</span>
            </div>
          ))
        ) : (
          <p className="no-users">No users found.</p>
        )}
      </div>
    </div>
  );
};

export default AllUsers;
