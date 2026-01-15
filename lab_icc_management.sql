-- -----------------------------
-- Create Database
-- -----------------------------
CREATE DATABASE IF NOT EXISTS lab_icc_management;
USE lab_icc_management;

-- -----------------------------
-- Users Table
-- -----------------------------
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student','technician','admin','icc_member') NOT NULL,
    department VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------
-- Labs Table
-- -----------------------------
CREATE TABLE labs (
    lab_id INT AUTO_INCREMENT PRIMARY KEY,
    lab_name VARCHAR(50) NOT NULL UNIQUE
);

-- -----------------------------
-- Lab Complaints Table
-- -----------------------------
CREATE TABLE lab_complaints (
    labcomplaint_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    lab_id INT NOT NULL,
    category ENUM(
        'Hardware Issue',
        'Software Issue',
        'Network Issue',
        'Cleanliness',
        'Power Backup / UPS',
        'Safety Issue'
    ) NOT NULL,
    description TEXT NOT NULL,
    image_path VARCHAR(255),
    status ENUM('Submitted','In Progress','Resolved','Closed') DEFAULT 'Submitted',
    assigned_to INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (lab_id) REFERENCES labs(lab_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL
);

-- -----------------------------
-- ICC Panel Table
-- -----------------------------
CREATE TABLE icc_panel (
    panel_id INT AUTO_INCREMENT PRIMARY KEY,
    panel_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------
-- ICC Panel Members Table
-- -----------------------------
CREATE TABLE icc_panel_members (
    panel_member_id INT AUTO_INCREMENT PRIMARY KEY,
    panel_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (panel_id) REFERENCES icc_panel(panel_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- -----------------------------
-- ICC Complaints Table
-- -----------------------------
CREATE TABLE icc_complaints (
    icccomplaint_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    panel_id INT NOT NULL,
    type ENUM(
        'Harassment',
        'Bullying',
        'Misconduct',
        'Discrimination',
        'Verbal Abuse',
        'Physical Threats',
        'Gender-based issues'
    ) NOT NULL,
    description TEXT NOT NULL,
    incident_date DATE NOT NULL,
    evidence_path VARCHAR(255),
    status ENUM('Filed','Under Review','Meeting Scheduled','Resolved') DEFAULT 'Filed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (panel_id) REFERENCES icc_panel(panel_id) ON DELETE CASCADE
);

-- -----------------------------
-- Notifications Table
-- -----------------------------
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Read','Unread') DEFAULT 'Unread',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
