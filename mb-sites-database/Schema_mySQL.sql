CREATE DATABASE meeting_app_db;

USE meeting_app_db;

CREATE TABLE users (
  id CHAR(36) NOT NULL,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE bookings (
  id CHAR(36) NOT NULL,
  guest_name VARCHAR(255) NOT NULL,
  guest_email VARCHAR(255) NOT NULL,
  reason TEXT,
  meeting_time DATETIME NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

INSERT INTO users (id, name, email, password)
VALUES (UUID(), 'John Doe', 'john@example.com', 'hashed_password_123');

SELECT * FROM users;
