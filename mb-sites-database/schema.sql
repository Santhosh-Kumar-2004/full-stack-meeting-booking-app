CREATE DATABASE meeting_app_db;

USE meeting_app_db;

CREATE TABLE users (
  id CHAR(36) NOT NULL,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);