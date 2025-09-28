## 🌍 Flow of One Request (Example: Booking a Meeting)

### Frontend → Register
    User submits form → POST /register.
    Data validated → stored in DB.

### Frontend → Login
    User submits credentials → POST /login.
    If valid → backend returns JWT token.

### Frontend → Create Booking
    User clicks “Book Meeting” → POST /bookings/create.
    Request must include Authorization: Bearer <token>.
    Backend extracts user from token (get_current_user).

### Booking saved in DB.
    Admin → See All Bookings
    Admin logs in with registered admin email.
    
### Calls GET /bookings/all.
    get_current_user confirms admin role → returns all bookings.