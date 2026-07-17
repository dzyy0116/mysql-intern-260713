# 第一周：MySQL+Python交互
## 运行环境
MacOS + MySQL 8.0 + Python3 + pymysql
## 文件说明
1. sql/init.sql：完整初始化脚本，包含创建数据库、学生表、全套增删改查SQL
2. db_helper.py：封装通用MySqlHelper工具类，自动管理连接、事务、异常，使用者仅需传入SQL和参数
3. requirements.txt：项目依赖包列表
## 运行步骤
1. 本地启动MySQL服务，在mysql命令行执行sql/init.sql初始化数据表
2. 修改db_helper.py中MySQL root登录密码
3. 终端进入项目目录，执行 python3 db_helper.py 测试全部CRUD功能
## 第三周：豆瓣电影TOP100爬虫
### 字段设计依据（可视化图表需求）
1. movie_rank：用于榜单排行图表
2. release_year / region：柱状图统计不同年份、地区电影数量
3. movie_type：饼图展示各影片类型占比
4. score、vote_count：散点图分析评分与评价人数的热度关系
### 运行脚本
python3 douban_movie_spider.py
### 实现逻辑
复用第一周封装的MySqlHelper数据库工具类，分页爬取豆瓣TOP250前100条电影，做数据容错清洗后存入可视化专用数据表。
## 第四周：React + Flask 前后端基础联调
1. 后端：flask搭建接口，flask-cors解决跨域，提供GET、POST两个测试接口
2. 前端：create-react-app构建页面，3个输入框、2个功能按钮
   - GET接口：读取输入框1作为URL查询参数，后端返回拼接字符串
   - POST接口：输入框2存入请求Body JSON，输入框3作为URL参数，后端同时接收两类参数并返回
3. 启动方式
   后端：cd flask_backend && python3 app.py
   前端：cd react_frontend && npm start