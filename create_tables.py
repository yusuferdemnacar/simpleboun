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

cursor.execute("DELIMITER $$")
cursor.execute("""
CREATE TRIGGER GradeTrigger 
AFTER INSERT ON Grade 
FOR EACH ROW 
BEGIN 

DECLARE credits_taken INT unsigned DEFAULT 1; 

SELECT C.credits 
INTO credits_taken 
FROM Course C WHERE 
C.course_id = NEW.course_id; 

UPDATE Student SET gpa = (gpa*completed_credits + NEW.grade*credits_taken)/(completed_credits + credits_taken), completed_credits = completed_credits + credits_taken 
WHERE student_id = NEW.student_id; 
END$$
""")
cursor.execute("DELIMITER ;")

cursor.execute("DELIMITER $$")
cursor.execute("""
CREATE TRIGGER ScheduleTrigger 
BEFORE INSERT ON Schedule 
FOR EACH ROW 
BEGIN 

DECLARE CCapacity INT unsigned DEFAULT 0; 
DECLARE CQuota INT unsigned DEFAULT 0; 

SELECT C.capacity 
INTO CCapacity 
FROM Classroom C 
WHERE C.classroom_id = NEW.classroom_id; 

SELECT C.quota 
INTO CQuota 
FROM Course C 
WHERE C.course_id = NEW.course_id; 

IF CCapacity < CQuota THEN 

DELETE FROM Plan P 
WHERE P.classroom_id = NEW.classroom_id AND P.slot = NEW.slot; 

DELETE FROM Lectured_by L 
WHERE L.course_id = NEW.course_id; 
DELETE FROM Course C WHERE C.course_id = NEW.course_id; 

signal sqlstate '45000'; 

END IF; 

END$$
""")
cursor.execute("DELIMITER ;")

cursor.execute("DELIMITER $$")
cursor.execute("""
CREATE TRIGGER FourManagers
BEFORE INSERT ON Database_manager
FOR EACH ROW
BEGIN

DECLARE manager_amount INT unsigned DEFAULT 0;
SELECT COUNT(*)
INTO manager_amount
FROM Database_manager;

IF manager_amount > 3
THEN

signal sqlstate '45000';

END IF;

END$$
""")
cursor.execute("DELIMITER ;")

cursor.exeute("""
CREATE TRIGGER EnrollTrigger
BEFORE INSERT ON Enrolled
FOR EACH ROW
BEGIN
    DECLARE taken_prerequisites INT unsigned DEFAULT 0;
    DECLARE prerequisite_count INT unsigned DEFAULT 0;
    DECLARE is_enrolled INT unsigned DEFAULT 0;
    DECLARE course_quota INT unsigned DEFAULT 0;
    DECLARE enrolled_students INT unsigned DEFAULT 0;


    SELECT COUNT(*)
    INTO taken_prerequisites
    FROM    (SELECT DISTINCT P.prerequisite_id
        FROM Prerequisite P INNER JOIN Grade G ON G.course_id = P.prerequisite_id
        WHERE P.course_id = NEW.course_id) AS Q
    WHERE Q.prerequisite_id IN    (SELECT K.course_id
                        FROM Grade K
                        WHERE K.student_id = NEW.student_id);

    SELECT COUNT(*)
    INTO prerequisite_count
    FROM Prerequisite P
    WHERE P.course_id = NEW.course_id;

    SELECT COUNT(*)
    INTO is_enrolled
    FROM Enrolled E
    WHERE E.student_id = NEW.student_id AND E.course_id = NEW.course_id;

    SELECT COUNT(*)
    INTO enrolled_students
    FROM Enrolled E
    WHERE E.course_id = NEW.course_id;

    SELECT C.quota
    INTO course_quota
    FROM Course C
    WHERE C.course_id = NEW.course_id;

    IF taken_prerequisites != prerequisite_count OR enrolled_students >= course_quota THEN

    signal sqlstate '45000';
    END IF;
END$$
""")

connection.commit()

#Create stored procedure

cursor.execute("DELIMITER $$")
cursor.execute("""
CREATE PROCEDURE FilterCourses(IN dep_id VARCHAR(200), IN cmps VARCHAR(200),
IN min_credits INT, IN max_credits INT)
BEGIN
    SELECT C.course_id, C.name, I.surname, I.department_id, C.credits,
        S.classroom_id, S.slot, C.quota, GROUP_CONCAT(P.prerequisite_id)
    FROM ((((Course C INNER JOIN Lectured_by L ON L.course_id = C.course_id)
        INNER JOIN Instructor I ON L.username = I.username)
        INNER JOIN Schedule S ON S.course_id = C.course_id)
        INNER JOIN Classroom R ON R.classroom_id = S.classroom_id)
        LEFT OUTER JOIN Prerequisite P ON P.course_id = C.course_id
    WHERE I.department_id = dep_id AND R.campus = cmps 
        AND C.credits >= min_credits AND C.credits <= max_credits
    GROUP BY C.course_id;
END $$
""")
cursor.execute("DELIMITER ;")

connection.commit()
