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

-- 第三周任务：豆瓣TOP100电影表
CREATE TABLE douban_movie_top100 (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
    movie_rank INT NOT NULL COMMENT '榜单排名（排行图表）',
    movie_name VARCHAR(255) NOT NULL COMMENT '电影名称',
    director VARCHAR(100) NOT NULL COMMENT '导演',
    actors TEXT COMMENT '主演列表',
    release_year INT NOT NULL COMMENT '上映年份（年份分布柱状图）',
    region VARCHAR(50) COMMENT '制片地区（地区统计柱状图）',
    movie_type VARCHAR(100) NOT NULL COMMENT '影片类型（类型占比饼图）',
    runtime INT COMMENT '片长(分钟)',
    score DECIMAL(3,1) NOT NULL COMMENT '豆瓣评分（评分散点图）',
    vote_count INT NOT NULL COMMENT '评价人数（热度散点图）',
    intro TEXT COMMENT '影片简介',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '爬取入库时间'
) COMMENT='豆瓣电影TOP100 可视化专用数据表';