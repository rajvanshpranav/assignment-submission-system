Create Database OASIS;
USE OASIS;
-- COURSES
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    instructor_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STUDENTS
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    course_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- ASSIGNMENTS
CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    deadline DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- SUBMISSIONS
CREATE TABLE submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    assignment_id INT NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    submission_time DATETIME NOT NULL,
    status ENUM('on-time', 'late') DEFAULT 'on-time',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id)
);

-- PROCESSED SUBMISSIONS
CREATE TABLE processed_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    submission_id INT,
    student_id INT,
    assignment_id INT,
    submission_time DATETIME,
    deadline DATETIME,
    submission_delay_minutes INT,
    is_late boolean,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DAILY SUMMARY
CREATE TABLE daily_submission_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    total_submissions INT,
    on_time_submissions INT,
    late_submissions INT,
    late_percentage FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STUDENT SUMMARY
CREATE TABLE student_activity_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    total_submissions INT,
    late_submissions INT,
    on_time_submissions INT,
    late_ratio FLOAT,
    last_submission DATETIME,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

show tables;

INSERT INTO courses (course_name, instructor_name) VALUES
('Data Engineering', 'Dr. Kaleen'),
('Database Systems', 'Prof. CBUM');

INSERT INTO students (name, email, course_id) VALUES
('Nobel Mateo da Vinci', 'nobel@gmail.com', 1),
('Bhalu Dwivedi', 'bhalu@gmail.com', 1),
('Pallab Bangali', 'pallab@gmail.com', 2),
('Surjit Sleep', 'surjit@gmail.com', 2);

INSERT INTO assignments (course_id, title, description, deadline) VALUES
(1, 'ETL Pipeline Design', 'Design a basic ETL pipeline', '2026-04-18 23:59:00'),
(1, 'Data Modeling', 'Create ER diagram', '2026-04-19 23:59:00'),
(2, 'SQL Queries', 'Practice advanced SQL', '2026-04-18 20:00:00');

INSERT INTO submissions (student_id, assignment_id, file_path, submission_time, status) VALUES
(1, 1, '/data/raw/nobel_etl.pdf', '2026-04-18 22:00:00', 'on-time'),
(2, 1, '/data/raw/bhalu_etl.pdf', '2026-04-19 00:30:00', 'late'),
(3, 3, '/data/raw/pallab_sql.pdf', '2026-04-18 19:00:00', 'on-time'),
(4, 3, '/data/raw/surjit_sql.pdf', '2026-04-18 21:00:00', 'late');

SELECT * FROM courses;
SELECT * FROM students;
SELECT * FROM assignments;
SELECT * FROM submissions;







