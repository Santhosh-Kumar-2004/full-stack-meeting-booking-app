import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import "../styles/MyBookings.css";

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchMyBookings = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      toast.error("Please login first!");
      navigate("/login");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/bookings/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 401) {
        toast.error("Session expired. Please login again.");
        localStorage.removeItem("token");
        navigate("/login");
        return;
      }

      if (!response.ok) {
        throw new Error("Failed to fetch your bookings");
      }

      const data = await response.json();
      setBookings(data);
    } catch (error) {
      console.error("Error fetching user bookings:", error);
      toast.error("Error fetching bookings");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id) => {
    const token = localStorage.getItem("token");

    if (!window.confirm("Do you really want to cancel this booking?")) return;

    try {
      const response = await fetch(`http://localhost:8000/bookings/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to cancel booking");
      }

      setBookings((prev) => prev.filter((b) => b.id !== id));
      toast.success("Booking cancelled successfully");
    } catch (error) {
      toast.error(error.message);
    }
  };

  useEffect(() => {
    fetchMyBookings();
  }, []);

  if (loading) {
    return (
      <div className="mybookings-loading">
        <div className="loader"></div>
        <p>Loading your bookings...</p>
      </div>
    );
  }

  return (
    <div className="mybookings-page">
      <h1 className="mybookings-title">My Bookings</h1>

      {bookings.length === 0 ? (
        <p className="no-mybookings">You have no active bookings.</p>
      ) : (
        <div className="mybookings-grid">
          {bookings.map((booking) => (
            <div className="mybooking-card" key={booking.id}>
              <h3>{booking.meeting_title}</h3>
              <p><strong>Reason:</strong> {booking.reason}</p>
              <p><strong>Meeting Time:</strong> {new Date(booking.meeting_time).toLocaleString()}</p>
              <p><strong>Status:</strong> {booking.status || "Confirmed"}</p>

              <button
                className="cancel-btn"
                onClick={() => handleCancel(booking.id)}
              >
                Cancel
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyBookings;
