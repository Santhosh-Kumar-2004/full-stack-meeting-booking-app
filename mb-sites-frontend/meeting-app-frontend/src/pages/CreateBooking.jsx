import React, { useState } from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "../styles/CreateBooking.css";

const CreateBooking = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    guest_name: "",
    guest_email: "",
    reason: "",
    meeting_time: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    if (!token) {
      toast.error("Please login before booking a meeting!");
      navigate("/login");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/bookings/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Failed to create booking");
      }

      toast.success("Meeting booked successfully!");
      setFormData({
        guest_name: "",
        guest_email: "",
        reason: "",
        meeting_time: "",
      });
      navigate("/");
    } catch (error) {
      console.error("Error creating booking:", error);
      toast.error(error.message);
    }
  };

  return (
    <div className="create-booking-page">
      <div className="create-booking-card">
        <h2>Book a Meeting</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="guest_name"
            placeholder="Your Name"
            value={formData.guest_name}
            onChange={handleChange}
            required
          />

          <input
            type="email"
            name="guest_email"
            placeholder="Your Email"
            value={formData.guest_email}
            onChange={handleChange}
            required
          />

          <textarea
            name="reason"
            placeholder="Reason for Meeting"
            value={formData.reason}
            onChange={handleChange}
            required
          ></textarea>

          <input
            type="datetime-local"
            name="meeting_time"
            value={formData.meeting_time}
            onChange={handleChange}
            required
          />

          <button type="submit" className="btn-primary">
            Submit Booking
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateBooking;
