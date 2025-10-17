import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "../styles/AllBookings.css";

const AllBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Fetch all bookings (Admin only)
  const fetchBookings = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      toast.error("Please login as Admin");
      navigate("/login");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/bookings/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 403) {
        toast.error("You are not authorized to view bookings!");
        navigate("/");
        return;
      }

      if (!response.ok) {
        throw new Error("Failed to fetch bookings");
      }

      const data = await response.json();
      setBookings(data);
    } catch (error) {
      console.error("Error fetching bookings:", error);
      toast.error("Something went wrong while fetching bookings");
    } finally {
      setLoading(false);
    }
  };

  // Delete booking
  const handleDelete = async (id) => {
    const token = localStorage.getItem("token");

    if (!window.confirm("Are you sure you want to delete this booking?")) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/bookings/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to delete booking");
      }

      toast.success("Booking deleted successfully!");
      setBookings((prev) => prev.filter((b) => b.id !== id));
    } catch (error) {
      console.error("Error deleting booking:", error);
      toast.error(error.message);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  if (loading) {
    return (
      <div className="bookings-loading">
        <div className="loader"></div>
        <p>Loading bookings...</p>
      </div>
    );
  }

  return (
    <div className="bookings-page">
      <h1 className="bookings-title">All Bookings</h1>

      {bookings.length === 0 ? (
        <p className="no-bookings">No bookings found.</p>
      ) : (
        <div className="bookings-grid">
          {bookings.map((booking) => (
            <div className="booking-card" key={booking.id}>
              <h3>{booking.guest_name}</h3>
              <p><strong>Email:</strong> {booking.guest_email}</p>
              <p><strong>Reason:</strong> {booking.reason}</p>
              <p><strong>Time:</strong> {new Date(booking.meeting_time).toLocaleString()}</p>

              <button
                className="delete-btn"
                onClick={() => handleDelete(booking.id)}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AllBookings;
