import mysql.connector
import environ

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
  host=env("MYSQL_HOST"),
  user=env("MYSQL_USER"),
  password=env("MYSQL_PASSWORD"),
  database=env("MYSQL_DATABASE"),
  auth_plugin='mysql_native_password'
)

cursor= connection.cursor()

#Create tables

cursor.execute("""
CREATE TABLE IF NOT EXISTS Database_manager (
username varchar(200) NOT NULL,
password varchar(64) NOT NULL,
PRIMARY KEY(username)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Department (
depname varchar(200) NOT NULL,
department_id varchar(200) NOT NULL,
UNIQUE(depname),
PRIMARY KEY(department_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
username varchar(200) NOT NULL,
student_id INT NOT NULL,
department_id varchar(200) NOT NULL,
password varchar(64) NOT NULL,
name varchar(200) NOT NULL,
surname varchar(200) NOT NULL,
email varchar(200) NOT NULL,
completed_credits INT NOT NULL,
gpa FLOAT NOT NULL,
PRIMARY KEY(username),
UNIQUE(student_id),
FOREIGN KEY(department_id) REFERENCES Department(department_id)
);
""")

#Title cannot be any string

cursor.execute("""
CREATE TABLE IF NOT EXISTS Instructor (
username varchar(200) NOT NULL,
department_id varchar(200) NOT NULL,
title varchar(200) NOT NULL,
password varchar(64) NOT NULL,
name varchar(200) NOT NULL,
surname varchar(200) NOT NULL,
email varchar(200) NOT NULL,
PRIMARY KEY(username),
FOREIGN KEY(department_id) REFERENCES Department(department_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Course (
course_id varchar(200) NOT NULL,
name varchar(200) NOT NULL,
credits INT NOT NULL,
quota INT NOT NULL,
PRIMARY KEY(course_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Time_slot (
slot INT NOT NULL,
PRIMARY KEY(slot),
CHECK((slot < 11) AND (0 < slot))
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Classroom (
classroom_id varchar(200) NOT NULL,
capacity INT NOT NULL,
campus varchar(200),
PRIMARY KEY(classroom_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Grade (
grade FLOAT NOT NULL,
student_id INT NOT NULL,
course_id varchar(200) NOT NULL,
PRIMARY KEY(student_id, course_id),
FOREIGN KEY(student_id) REFERENCES Student(student_id),
FOREIGN KEY(course_id) REFERENCES Course(course_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrolled (
student_id INT NOT NULL,
course_id varchar(200) NOT NULL,
PRIMARY KEY(student_id, course_id),
FOREIGN KEY(student_id) REFERENCES Student(student_id),
FOREIGN KEY(course_id) REFERENCES Course(course_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Prerequisite (
course_id varchar(200) NOT NULL,
prerequisite_id	  varchar(64) NOT NULL,
PRIMARY KEY(course_id, prerequisite_id),
FOREIGN KEY(course_id) REFERENCES Course(course_id),
FOREIGN KEY(prerequisite_id) REFERENCES Course(course_id),
CHECK(course_id > prerequisite_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Lecturer_at (
username varchar(200) NOT NULL,
department_id varchar(200) NOT NULL,
PRIMARY KEY(username),
FOREIGN KEY(username) REFERENCES Instructor(username),
FOREIGN KEY(department_id) REFERENCES Department(department_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Lectured_by (
course_id varchar(200) NOT NULL,
username varchar(200) NOT NULL,
PRIMARY KEY(course_id),
FOREIGN KEY(username) REFERENCES Lecturer_at(username),
FOREIGN KEY(course_id) REFERENCES Course(course_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Plan (
classroom_id varchar(200) NOT NULL,
slot INT NOT NULL,
PRIMARY KEY(classroom_id, slot),
FOREIGN KEY(classroom_id) REFERENCES Classroom(classroom_id),
FOREIGN KEY(slot) REFERENCES Time_slot(slot)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Schedule (
classroom_id varchar(200) NOT NULL,
slot INT NOT NULL,
course_id varchar(200) NOT NULL,
PRIMARY KEY(course_id),
FOREIGN KEY(course_id) REFERENCES Course(course_id),
FOREIGN KEY(classroom_id, slot) REFERENCES Plan(classroom_id, slot)
);
""")

connection.commit()

#Create triggers

connection.commit()
