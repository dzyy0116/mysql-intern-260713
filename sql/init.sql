CREATE DATABASE student_db;

USE student_db;

CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '学号',
    name VARCHAR(20) NOT NULL COMMENT '姓名',
    height FLOAT COMMENT '身高'
);

INSERT INTO student(name, height) VALUES 
('张三', 175.5),
('李四', 180.2),
('王五', 168.0);

SELECT * FROM student;

SELECT * FROM student WHERE id = 1;

UPDATE student SET height=176 WHERE id=1;

DELETE FROM student WHERE id=3;