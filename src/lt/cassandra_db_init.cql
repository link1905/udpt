CREATE KEYSPACE IF NOT EXISTS students_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE students_keyspace;

CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY,
    name TEXT,
    birthday DATE,
    activity_class TEXT,
    department_name TEXT,
    major_name TEXT,
    GPA FLOAT
);

CREATE TABLE IF NOT EXISTS students_by_department_name (
    department_name TEXT,
    id UUID,
    name TEXT,
    birthday DATE,
    activity_class TEXT,
    major_name TEXT,
    GPA FLOAT,
    PRIMARY KEY ((department_name), id)
);
CREATE TABLE IF NOT EXISTS students_by_activity_class (
    department_name TEXT,
    id UUID,
    name TEXT,
    birthday DATE,
    activity_class TEXT,
    major_name TEXT,
    GPA FLOAT,
    PRIMARY KEY ((activity_class), id)
);

CREATE TABLE IF NOT EXISTS classes (
    name TEXT PRIMARY KEY,
    department_name TEXT,
);

CREATE TABLE IF NOT EXISTS departments (
    name TEXT PRIMARY KEY,
    majors SET<TEXT>
);

INSERT INTO classes (name, department_name)
VALUES ('Class A', 'Department of Computer Science');
INSERT INTO classes (name, department_name)
VALUES ('Class B', 'Department of Electrical Engineering');
INSERT INTO departments (name, majors)
VALUES ('Department of Computer Science', { 'Computer Science', 'Software Engineering' });
INSERT INTO departments (name, majors)
VALUES ('Department of Electrical Engineering', { 'Electrical Engineering', 'Electronic Engineering' });