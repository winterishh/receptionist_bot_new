CREATE TABLE IF NOT EXISTS college_info (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);



CREATE TABLE IF NOT EXISTS departments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL,
    hod TEXT,
    description TEXT
);



CREATE TABLE IF NOT EXISTS faculty (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT,
    designation TEXT,
    email TEXT
);



CREATE TABLE IF NOT EXISTS courses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    duration TEXT,
    description TEXT
);



CREATE TABLE IF NOT EXISTS faq (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);